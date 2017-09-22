#!/bin/bash

echo "############################################################"
echo "This will replace the content of NYU_Notes"
echo "the most recent content from the Github repository"
echo ""
echo "The existing NYU_Notes folder will be renamed"
echo "NYU_Notes_"$(date '+%Y-%b-%d_%H%M')
echo "and preserved until you delete it. "
echo "############################################################"
echo ""
read -p "Are you sure that you want to proceed? (Y/N) " -n 1 -r
echo 
if [[ $REPLY =~ ^[Yy]$ ]]
then
  cd /home/ubuntu/jupyter
  mv NYU_Notes NYU_Notes_$(date '+%Y-%b-%d_%H%M')
  git clone https://github.com/ipeirotis/dealing_with_data.git NYU_Notes
  cd
fi

rm /home/ubuntu/sync_notebooks.sh 
ln -s /home/ubuntu/jupyter/NYU_Notes/sync_notebooks.sh /home/ubuntu/sync_notebooks.sh 
