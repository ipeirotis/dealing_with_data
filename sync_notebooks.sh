#!/bin/bash

echo "############################################################"
echo "This will delete the current content of NYU_Notes"
echo "and replace it with the content from the Github repository"
echo ""
echo "Please ensure that you have saved your own notebooks"
echo "into the Student_Notebooks folder"
echo "############################################################"
echo ""
read -p "Are you sure that you want to proceed? (Y/N) " -n 1 -r
echo    # (optional) move to a new line
if [[ $REPLY =~ ^[Yy]$ ]]
then
  cd /home/ubuntu/jupyter
  rm -rf NYU_Notes
  git clone https://github.com/ipeirotis/dealing_with_data.git NYU_Notes
  cd
fi

