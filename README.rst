===============================
BIDSonym
===============================

.. image:: https://img.shields.io/travis/PeerHerholz/BIDSonym.svg
        :target: https://travis-ci.org/PeerHerholz/BIDSonym

.. image:: https://img.shields.io/github/issues-pr/PeerHerholz/BIDSonym.svg
    :alt: PRs
    :target: https://github.com/PeerHerholz/BIDSonym/pulls/

.. image:: https://img.shields.io/github/contributors/PeerHerholz/BIDSonym.svg
    :alt: Contributors
    :target: https://GitHub.com/PeerHerholz/BIDSonym/graphs/contributors/

.. image:: https://github-basic-badges.herokuapp.com/commits/PeerHerholz/BIDSonym.svg
    :alt: Commits
    :target: https://github.com/PeerHerholz/BIDSonym/commits/master

.. image:: http://hits.dwyl.io/PeerHerholz/BIDSonym.svg
    :alt: Hits
    :target: http://hits.dwyl.io/PeerHerholz/BIDSonym

.. image:: https://img.shields.io/docker/cloud/automated/peerherholz/bidsonym
    :alt: Dockerbuild
    :target: https://cloud.docker.com/u/peerherholz/repository/docker/peerherholz/bidsonym

.. image:: https://img.shields.io/docker/pulls/peerherholz/bidsonym
    :alt: Dockerpulls
    :target: https://cloud.docker.com/u/peerherholz/repository/docker/peerherholz/bidsonym

.. image:: https://img.shields.io/badge/License-BSD%203--Clause-blue.svg
    :alt: License
    :target: https://opensource.org/licenses/BSD-3-Clause

.. image:: https://upload.wikimedia.org/wikipedia/commons/7/74/Zotero_logo.svg
    :alt: Zotero
    :target: https://www.zotero.org/groups/2362367/bidsonym


.. image:: https://img.shields.io/badge/Supported%20by-%20CONP%2FPCNO-red
    :alt: support_conp
    :target: https://conp.ca/

Description
===========
A `BIDS <https://bids-specification.readthedocs.io/en/stable/>`_ `app <https://bids-apps.neuroimaging.io/>`_ for the de-identification of neuroimaging data. ``BIDSonym`` gathers all T1w images from a BIDS dataset and applies one of several popular de-identification algorithms. It also helps deface T2w images by using defaced T1w image as deface-mask. It currently supports:

`MRI deface <https://surfer.nmr.mgh.harvard.edu/fswiki/mri_deface>`_, `Pydeface <https://github.com/poldracklab/pydeface>`_, `Quickshear <https://github.com/nipy/quickshear>`_, `mridefacer <https://github.com/mih/mridefacer>`_ and `deepdefacer <https://github.com/josai/DeepDeface>`_.

.. image:: https://raw.githubusercontent.com/PeerHerholz/BIDSonym/master/img/bidsonym_example.png
   :alt: alternate text

Additionally, the user can choose to evaluate the sidecar JSON files regarding potentially sensitive information,
like for example participant names and define a list of fields which information should be deleted.

**Using BIDSonym ensures that you can make collected neuroimaging data available for others without violating subjects' privacy or anonymity (depending on the regulations of the country you're in).**

.. intro-marker

Usage
=====

.. usage-marker

For more information on specific usage and commands, refer to the `SINAPSELAB manual <https://iowa-my.sharepoint.com/personal/johnsonhj_uiowa_edu/_layouts/OneNote.aspx?id=%2Fpersonal%2Fjohnsonhj_uiowa_edu%2FDocuments%2FSINAPSE_SHARED%2FSINAPSE_LAB_MANUAL&wd=target%28002%20-%20Lab%20Software%20Docs%2F002.4%20-%20End%20User%20Applications%2FBIDSonym.one%7C5D827DE8-4C68-4981-A87C-44AB6407E235%2F%29
/>`_.

This App has the following command line arguments:

usage: bidsonym [-h]
                [--participant_label PARTICIPANT_LABEL [PARTICIPANT_LABEL ...]]

                [--deid {pydeface,mri_deface,quickshear,mridefacer,deepdefacer}]

                [--deface_t2w DEFACE_T2W] [--del_nodeface {del,no_del}]

                [--check_meta CHECK_META [CHECK_META ...]]

                [--del_meta DEL_META [DEL_META ...]]

                [--brainextraction {bet,nobrainer}] [--bet_frac BET_FRAC] [-v]

                bids_dir {participant,group}

a BIDS app for de-identification of neuroimaging data

positional arguments:
  bids_dir              The directory with the input dataset formatted
                        according to the BIDS standard.
  {participant,group}   Level of the analysis that will be performed. Multiple
                        participant level analyses can be run independently
                        (in parallel) using the same output_dir.

optional arguments:
  --participant_label PARTICIPANT_LABEL [PARTICIPANT_LABEL ...]
                        The label(s) of the participant(s) that should be
                        analyzed. The label corresponds to
                        sub-<participant_label> from the BIDS spec (so it does
                        not include "sub-"). If this parameter is not provided
                        all subjects should be analyzed. Multiple participants
                        can be specified with a space separated list.

  --deid {pydeface,mri_deface,quickshear,mridefacer,deepdefacer}
                        Approach to use for de-identifictation.

  --deface_t2w DEFACE_T2W
                        Deface T2w images by using defaced T1w image as
                        deface-mask.

  --del_nodeface {del,no_del}
                        Overwrite and delete original data or copy original
                        data to sourcedata/.

  --check_meta CHECK_META [CHECK_META ...]
                        Indicate which information from the image and .json
                        meta-data files should be check for potentially
                        problematic information. Indicate strings that should
                        be searched for. The results will be saved to
                        sourcedata/

  --del_meta DEL_META [DEL_META ...]
                        Indicate if and which information from the .json meta-
                        data files should be deleted. If so, the original
                        .josn files will be copied to sourcedata/

  --brainextraction {bet,nobrainer}
                        What algorithm should be used for pre-defacing brain
                        extraction (outputs will be used in quality control).

  --bet_frac BET_FRAC   In case BET is used for pre-defacing brain extraction,
                        povide a Frac value.

  -v, --version         show program's version number and exit


Run it in participant level mode (for one participant):

.. code-block::

	docker run -i --rm \
		    -v /Shared/sinapse/chdi_bids/PREDICTHD_BIDS:/bids_dataset \
	            sinapselab/bidsonym \
		    /bids_dataset \
		    participant --deid pydeface --del_nodeface no_del --del_meta 'InstitutionAddress' \
		    --participant_label 000410


Run it in group level mode (for all participants):

.. code-block::

	docker run -i --rm \
		   -v /Shared/sinapse/chdi_bids/PREDICTHD_BIDS:/bids_dataset \
		   sinapselab/bidsonym \
		   /bids_dataset  group --deid pydeface --del_meta 'InstitutionAddress'

.. usage-marker-end


Installation
============
Following the `BIDS apps standard <https://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1005209>`_ it is recommend to install and use BIDSonym in its Docker or Singularity form. \
To get the BIDSonym Docker image, you need to `install docker <https://docs.docker.com/install/>`_ and within the terminal of your choice type:

:code:`docker pull sinapselab/bidsonym`

:code:`docker pull sinapselab/deepdefacer`

`deepdefacer` is required as a separate image.

To get its Singularity version, you need to `install singularity <https://singularity.lbl.gov/all-releases>`_ and within the terminal of your choice type:

:code:`singularity pull docker://sinapselab/bidsonym`

Documentation
=============
BIDSOnym's documentation can be found `here <https://peerherholz.github.io/BIDSonym/>`_.

The SINAPSELAB `manual <https://iowa-my.sharepoint.com/personal/johnsonhj_uiowa_edu/_layouts/OneNote.aspx?id=%2Fpersonal%2Fjohnsonhj_uiowa_edu%2FDocuments%2FSINAPSE_SHARED%2FSINAPSE_LAB_MANUAL&wd=target%28002%20-%20Lab%20Software%20Docs%2F002.4%20-%20End%20User%20Applications%2FBIDSonym.one%7C5D827DE8-4C68-4981-A87C-44AB6407E235%2F%29
/>`_ provides information on SINAPSELAB's version of BIDSonym.


Support
=======
This work is supported in part by funding provided by `Brain Canada <https://braincanada.ca/>`_, in partnership with `Health Canada <https://www.canada.ca/en/health-canada.html>`_, for the `Canadian Open Neuroscience Platform initiative <https://conp.ca/>`_.

.. image:: https://conp.ca/wp-content/uploads/elementor/thumbs/logo-2-o5e91uhlc138896v1b03o2dg8nwvxyv3pssdrkjv5a.png
    :alt: logo_conp
    :target: https://conp.ca/
