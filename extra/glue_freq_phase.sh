#!/bin/bash

IMGS="sine_tests/freq_phase"
DIR="sine_tests/freq_phase/results"

if [[ ! -d ${DIR} ]]; then
    mkdir ${DIR}
fi

for i in {1..10}; do
    montage ${IMGS}/${i}_-30.jpg ${IMGS}/${i}_-45.jpg -tile 2x1 -geometry +0+0 ${IMGS}/row_${i}.jpg
    COUNT=-60
    while [[ $COUNT -ge -90 ]]; do
        montage ${IMGS}/row_${i}.jpg ${IMGS}/${i}_${COUNT}.jpg -tile 2x1 -geometry +0+0 ${IMGS}/row_${i}.jpg
        COUNT=$((COUNT-15))
    done
done

echo "created rows; sleeping for 3 seconds before continuing"
sleep 3

montage ${IMGS}/row_1.jpg ${IMGS}/row_2.jpg -tile 1x2 -geometry +0+0 ${DIR}/result_1-5.jpg
for i in {3..5}; do
    montage ${DIR}/result_1-5.jpg ${IMGS}/row_${i}.jpg -tile 1x2 -geometry +0+0 ${DIR}/result_1-5.jpg
    sleep 2
done
echo "finished result file for rows 1-5"

montage ${IMGS}/row_6.jpg ${IMGS}/row_7.jpg -tile 1x2 -geometry +0+0 ${DIR}/result_6-10.jpg
for i in {8..10}; do
    montage ${DIR}/result_6-10.jpg ${IMGS}/row_${i}.jpg -tile 1x2 -geometry +0+0 ${DIR}/result_6-10.jpg
    sleep 2
done

echo "done!"
