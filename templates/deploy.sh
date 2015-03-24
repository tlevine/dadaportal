#!/bin/sh
set -e

echo Running the tests
./manage.py test

echo Copying canonical articles to nsa
rsync -avHS ./canonical-articles/ \
  nsa:{{ nsa_base_dir }}/canonical-articles # no slash at end

echo Caching the articles on nsa
ssh nsa 'cd {{ nsa_base_dir }} && ./manage.py syncarticles'

echo Indexing the articles on nsa
ssh nsa 'cd {{ nsa_base_dir }} && ./manage.py indexarticles'

echo Copy pal.conf to nsa
rsync -avHS {{ local_pal_conf }} nsa:{{ nsa_pal_conf }}

echo Copying pal calendar files to nsa
rsync -avHS {{ local_pal_dir }} nsa:{{ nsa_pal_dir }}

echo Generatiing static files on nsa
ssh nsa 'cd {{ nsa_base_dir }} && ./manage.py collectstatic'
