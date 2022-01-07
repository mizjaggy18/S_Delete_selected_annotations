# -*- coding: utf-8 -*-

# * Copyright (c) 2009-2018. Authors: see NOTICE file.
# *
# * Licensed under the Apache License, Version 2.0 (the "License");
# * you may not use this file except in compliance with the License.
# * You may obtain a copy of the License at
# *
# *      http://www.apache.org/licenses/LICENSE-2.0
# *
# * Unless required by applicable law or agreed to in writing, software
# * distributed under the License is distributed on an "AS IS" BASIS,
# * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# * See the License for the specific language governing permissions and
# * limitations under the License.

__author__ = "WSH Munirah W Ahmad 29 Dec 2021 <wshmunirah@gmail.com>"
__copyright__ = "Apache 2 license. Made by Multimedia University Cytomine Team, Cyberjaya, Malaysia, http://cytomine.mmu.edu.my/"
__version__ = "1.0.0"

import logging
import sys
from argparse import ArgumentParser

from shapely.geometry import Point, box

import cytomine
from cytomine.models import Property, Annotation, AnnotationTerm, AnnotationCollection, JobData, Job, TermCollection, ImageInstanceCollection


def run(cyto_job, parameters):
    logging.info("----- Delete selected annotations v%s -----", __version__)
    logging.info("Entering run(cyto_job=%s, parameters=%s)", cyto_job, parameters)

    job = cyto_job.job
    project = cyto_job.project        

    terms = TermCollection()
    terms.project = project.id
    terms.fetch_with_filter("project", project.id)
    job.update(status=Job.RUNNING, progress=1, statusComment="Terms gathered...")

    list_terms = []
    if parameters.cytomine_id_terms == 'all':
        for term in terms:
            list_terms.append(int(term.id))
    else:
        list_terms = parameters.cytomine_id_terms
        list_terms2 = list_terms.split(',')

    print('Input param:', parameters.cytomine_id_terms)
    print('Print list terms:', list_terms)
    print(type(list_terms))
    # list_imgs2 = list_terms.split(',')
    print(type(list_terms2))
    print('Print list terms2:', list_terms2)
    # for id_image in list_imgs2:
    #     print(id_image) 

    images = ImageInstanceCollection().fetch_with_filter("project", project.id)
    # conn.job.update(status=Job.RUNNING, progress=2, statusComment="Images gathered...")
    job.update(status=Job.RUNNING, progress=2, statusComment="Images gathered...")
    
    # print('images id:',images)

    list_imgs = []
    if parameters.cytomine_id_images == 'all':
        for image in images:
            list_imgs.append(int(image.id))
    else:
        list_imgs = parameters.cytomine_id_images
        list_imgs2 = list_imgs.split(',')
        
    print('Input param:', parameters.cytomine_id_images)
    print('Print list images:', list_imgs)
    print(type(list_imgs))
    # list_imgs2 = list_imgs.split(',')
    print(type(list_imgs2))
    print('Print list images2:', list_imgs2)
    # for id_image in list_imgs2:
    #     print(id_image) 

    #Go over images
    for (i, id_image) in enumerate(list_imgs2):  
        progress=2+i
        for id_term in list_terms2:
            # Get the list of annotations
            annotations = AnnotationCollection()
            annotations.image = id_image
            annotations.term = id_term
            annotations.project = project.id
            annotations.fetch()
            print("Total annotations: ",len(annotations))
            if len(annotations) > 0:
                progress_delta=100-(progress)/len(annotations)
            else:
                progress_delta=100-(progress)/len(list_imgs2)

            for annotation in annotations:
                progress += progress_delta
                job.update(status=Job.RUNNING, progress=progress, statusComment="Deleting %s from %s..." % (str(annotation.id),str(id_image)))
                annotation.delete()
                

if __name__ == "__main__":
    logging.debug("Command: %s", sys.argv)

    with cytomine.CytomineJob.from_cli(sys.argv) as cyto_job:
        run(cyto_job, cyto_job.parameters)
