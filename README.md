# MeHEDI-app | An Healthcare Data-Driven

## 0.Pre-processing and Segmentation

### Semi-automatic method for Pre-processing 

This folder contain the workflow used for preprocessing T1-W images. 

![Preprocessing_giusto drawio](https://user-images.githubusercontent.com/78934727/142078775-1a50e3ad-7be1-4b12-bf15-ff93dcb0eb70.png)

### Plot histogram subjects (without background)

In this plot, there is a comparison between the different distribution curve of categorical subjects.
In particular, we observe a big curve distribution difference in the case of high distorted case.
Furthermore, it is interesting to note that in the case of a distorted subject from another 
category the tissue distribution curve is quite similar to that of a healthy subject.

![Untitled Diagram drawio](https://user-images.githubusercontent.com/78934727/143457592-504aa93f-05f3-4dc1-af7f-a5ff125a93f3.png)

### Why use a thresholding method with manual selection of the thresholds?

Why was it necessary to use a Threshold segmentation method with choice of manual thresholds compared for example to the Otsu segmentation method (automatic thresholds that minimize intra-class variance)?
The script multi-otsu creates a segmentation based on Otsu method.

![COMPARAZIONE_288618_totale](https://user-images.githubusercontent.com/78934727/144195381-34d38aae-2ca7-4fa9-9a72-a874568b148a.png)

The comparison between the two segmentation methods highlights a gross segmentation by the automatic segmentation algorithm in the case of subjects with severe brain malformations. This is confirmed by the calculation of the Dice Score metric which reports very low results for the Otsu segmentation, in particular for the recognition of background and CSF.

![comparison_method2 drawio](https://user-images.githubusercontent.com/78934727/144581503-b270da5f-ed2b-4652-934f-ea7ab42e9273.png)

### Semi-automatic method for Segmentation 

It also contains a .txt file describing the workflow used for tissue segmentation using 
the ITKSNAP software CLI. In particular, using two different algorithms: Thresholding and Clustering.

![segmentation](https://user-images.githubusercontent.com/78934727/142191006-f16cdb4e-0eef-48f1-bf62-bd1b57f991d8.png)

![clustering](https://user-images.githubusercontent.com/78934727/142191087-ec51bbe9-c201-4bfa-8368-c3516a9d5caf.png)

![Trunk_Cerebellum_Segmentation drawio](https://user-images.githubusercontent.com/78934727/143455141-9688d757-23a8-4869-8b80-dd9e8859d3d7.png)


