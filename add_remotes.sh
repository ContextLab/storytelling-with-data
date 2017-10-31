#!/bin/bash

echo YOU SHOULD RUN THIS FROM WITHIN DOCKER!!

cd /mnt/storytelling-with-data

echo adding class repo as upstream
git remote add upstream https://github.com/ContextLab/storytelling-with-data.git

echo adding each students repo, by student first name
git remote add jeremy https://github.com/jeremymanning/storytelling-with-data.git
git remote add campbell https://github.com/campbellfield/storytelling-with-data.git
git remote add shinar https://github.com/shinarjain/storytelling-with-data.git
git remote add steven https://github.com/coachharney/storytelling-with-data.git
git remote add jane https://github.com/jjanelee97/storytelling-with-data.git
git remote add lillian https://github.com/lillianzhao/storytelling-with-data.git
git remote add ariana https://github.com/ArianaMoran/storytelling-with-data.git
git remote add ellie https://github.com/ebennett10/storytelling-with-data.git
git remote add cameron https://github.com/camartin95/storytelling-with-data.git
git remote add isabelle https://github.com/igleonaitis/storytelling-with-data.git

echo done.
