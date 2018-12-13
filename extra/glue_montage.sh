#!/bin/bash

if [[ ! -z $(find generating_images_demo/ -name "row*") ]]; then
    echo "found row* images to delete in generating_images_demo"
    rm generating_images_demo/row*
fi

for i in {0..20}; do
    montage generating_images_demo/modulate_${i}_0.jpg generating_images_demo/modulate_${i}_1.jpg -tile 2x1 -geometry +0+0 generating_images_demo/row_${i}.jpg
    for j in {2..20}; do
        montage generating_images_demo/row_${i}.jpg generating_images_demo/modulate_${i}_${j}.jpg -tile 2x1 -geometry +0+0 generating_images_demo/row_${i}.jpg
    done
    # montage generating_images_demo/modulate_${i}_[0-20].jpg -tile 21x1 -geometry +0+0 generating_images_demo/row_${i}.jpg
    echo "finished generating row file for row $i"
    # convert append generating_images_demo/modulate_${i}_*.jpg generating_images_demo/row_${i}.jpg
done

montage generating_images_demo/row_0.jpg generating_images_demo/row_1.jpg -tile 1x2 -geometry +0+0 generating_images_demo/result.jpg
while [[ ! -e generating_images_demo/result.jpg ]]; do
    echo "waiting for result.jpg to be generated"
    sleep 1
done

for i in {2..20}; do 
    mv generating_images_demo/result.jpg generating_images_demo/tmp.jpg
    while [[ ! -e generating_images_demo/tmp.jpg || -e generating_images_demo/result.jpg ]]; do
        echo "waiting for result.jpg to be moved to tmp.jpg"
        sleep 1
    done
    sleep 10
    montage generating_images_demo/tmp.jpg generating_images_demo/row_${i}.jpg -tile 1x2 -geometry +0+0 generating_images_demo/result.jpg
    sleep 10
    while [[ ! -e generating_images_demo/result.jpg ]]; do
        echo "waiting for result.jpg to be regenerated"
        sleep 1
    done
    rm generating_images_demo/tmp.jpg
done

mv generating_images_demo/result.jpg generating_images_demo/big_result.jpg
rm generating_images_demo/row*.*
