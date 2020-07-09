#!/usr/bin/env python3
import argparse
import os
from subprocess import check_call
import nibabel
import numpy
from glob import glob
import nipype.pipeline.engine as pe
from nipype.interfaces import utility as niu
from nipype.interfaces.quickshear import Quickshear
from nipype.interfaces.fsl import BET
from shutil import copy, move

__version__ = open(
    os.path.join(os.path.dirname(os.path.realpath(__file__)), "version")
).read()

# define function for pydeface
def run_pydeface(image, outfile):
    # pydeface $image --outfile $outfile
    cmd = ["pydeface", image, "--out", outfile, "--force"]
    check_call(cmd)
    return


# define function for mri_deface
def run_mri_deface(image, brain_template, face_template, outfile):
    # mri_deface $image $brain_template $face_template $outfile
    cmd = ["mri_deface", image, brain_template, face_template, outfile]
    check_call(cmd)
    return


# define function for quickshear
# based on the nipype docs quickshear example
def run_quickshear(image, outfile):
    # quickshear anat_file mask_file defaced_file [buffer]
    deface_wf = pe.Workflow("deface_wf")
    inputnode = pe.Node(niu.IdentityInterface(["in_file"]), name="inputnode")
    outputnode = pe.Node(niu.IdentityInterface(["out_file"]), name="outputnode")
    bet = pe.Node(BET(mask=True, frac=0.5), name="bet")
    quickshear = pe.Node(Quickshear(buff=50), name="quickshear")
    deface_wf.connect(
        [
            (inputnode, bet, [("in_file", "in_file")]),
            (inputnode, quickshear, [("in_file", "in_file")]),
            (bet, quickshear, [("mask_file", "mask_file")]),
        ]
    )
    inputnode.inputs.in_file = image
    quickshear.inputs.out_file = outfile
    res = deface_wf.run()


def run_mridefacer(image):
    cmd = ["mridefacer/mridefacer", "--apply", image]
    check_call(cmd)
    return


def run_all(filename, methods):
    # the -7 removes the extension ".nii.gz" from the filename
    if "pydeface" in methods:
        pydefaced = filename[:-7] + "_pydeface.nii.gz"
        if not os.path.exists(pydefaced):
            copy(filename, pydefaced)
            run_pydeface(pydefaced, pydefaced)
    # This is inside a try catch block because it can fail sometimes due to Numerical Instability
    if "mri_deface" in methods:
        defaceDone = False
        try:
            mri_defaced = filename[:-7] + "_mri_deface.nii.gz"
            if not os.path.exists(mri_defaced):
                copy(filename, mri_defaced)
                run_mri_deface(
                    mri_defaced,
                    "/home/fs_data/talairach_mixed_with_skull.gca",
                    "/home/fs_data/face.gca",
                    mri_defaced,
                )
            defaceDone = True
        except:
            pass
        for lowPercentile in [1, 3, 5]:
            try:
                if not defaceDone:
                    import SimpleITK as sitk
                    import numpy as np
                    img = sitk.ReadImage(filename)
                    arr = sitk.GetArrayFromImage(img)
                    low = np.percentile(arr, lowPercentile)
                    high = np.percentile(arr, 100 - lowPercentile)
                    clamp = sitk.ClampImageFilter()
                    clamp.SetLowerBound(low)
                    clamp.SetUpperBound(high)
                    img_modified = clamp.Execute(img)
                    sitk.WriteImage(img_modified, filename[:-7] + '_modified.nii.gz')
                    run_mri_deface(
                        filename[:-7] + '_modified.nii.gz',
                        "/home/fs_data/talairach_mixed_with_skull.gca",
                        "/home/fs_data/face.gca",
                        filename[:-7] + "_mri_deface.nii.gz",
                    )
                    os.remove(filename[:-7] + '_modified.nii.gz')
                    defaceDone = True
            except:
                pass
        if not defaceDone:
            try:
                file = open('/' + filename.split('/')[1] + '/tmp/mri_deface.log', 'a')
                file.write("Error in defacing: /" + '/'.join(filename.split('/')[2:]) + '\n')
                file.close()
            except:
                pass
    if "quickshear" in methods:
        quicksheared = filename[:-7] + "_quickshear.nii.gz"
        if not os.path.exists(quicksheared):
            copy(filename, quicksheared)
            run_quickshear(quicksheared, quicksheared)
    if "mridefacer" in methods:
        mridefacered = filename[:-7] + "_mridefacer.nii.gz"
        if not os.path.exists(mridefacered):
            copy(filename, mridefacered)
            run_mridefacer(mridefacered)


if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        description="Tool to use various defacing algorithms on NIFTI_GZ images"
    )
    parser.add_argument(
        "--filename",
        help="this needs to be an absolute path to the image as it would be inside the docker container.",
        required=True,
    )
    parser.add_argument(
        "--methods",
        nargs="+",
        default=["pydeface", "mri_deface", "quickshear", "mridefacer"],
        help="the list of different methods to apply on the input image. "
        "Options are pydeface, mri_deface, quickshear, mridefacer",
    )
    args = parser.parse_args()
    for i in args.methods:
        assert i in ["pydeface", "mri_deface", "quickshear", "mridefacer"]
    run_all(args.filename, args.methods)
