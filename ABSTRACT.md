The authors present **DeepSportRadar Instance Segmentation Challenge v.2 Dataset**, a comprehensive set comprising computer vision tasks, datasets, and benchmarks designed for automating sport comprehension. The primary aim of this dataset is to bridge the divide between academic research and real-world applications. In pursuit of this goal, the datasets include high-resolution raw images, camera parameters, and meticulously crafted annotations of superior quality. DeepSportradar currently addresses four demanding tasks pertaining to basketball: 

* **Ball 3D localization in calibrated scenes.** This task tackles the estimation of ball size on basketball scenes given the oracle ball position.
* **Camera calibration.** This task aims at predicting the camera calibration parameters from images taken from basketball games.
* **Player instance segmentation.** This task deals with the segmentation of individual humans (players, coaches and referees) on the basketball court.
* **Player re-identification.** In this task, the objective is to re-identify basketball players across multiple video frames captured from the same camera viewpoint at various time instants.

**Note:** the presented information on DatasetNinja is related to the instance segmentation task, but you can always refer to the [original data](https://www.kaggle.com/datasets/deepsportradar/basketball-instants-dataset)

## Motivation

Individual and professional sports have long wielded significant influence over the economic, political, and cultural fabric of society. In terms of economics alone, this impact is poised for expansion, with the global sports market, encompassing services and goods offered by sports entities, projected to surge from $354.96 billion in 2021 to a staggering $707.84 billion in 2026. The online live-streaming sector, in particular, is forecasted to witness remarkable growth, with its value skyrocketing from $18.12 billion in 2020 to $87.34 billion in 2028. A driving force behind this growth trajectory is the rapid advancement of technology, reshaping the landscape of sports consumption.

Indeed, advancements in Computer Vision (CV) and Deep Learning (DL) present the opportunity to extract rich insights from live-streamed sporting events, enhancing the viewing experience for audiences and leagues alike. However, the efficacy and reliability of DL-based solutions hinge heavily upon the quantity and quality of the training data. Each sporting discipline poses unique challenges for the models, and the quality of annotations significantly impacts overall performance.

In recent years, the SoccerNet datasets have garnered attention in the CV community for their extensive data and benchmark models. Nevertheless, two principal concerns mar this initiative: Firstly, restricting focus solely to soccer limits the generalizability of results across other sports domains. Secondly, and more critically, SoccerNet annotations are derived from broadcast videos, presenting several limitations. These include limited spatial and temporal coverage due to camera movements and interruptions by replays or advertisements, lower image resolution compared to the original sensor, lack of access to camera parameters or positioning data, and the presence of overlay graphics such as scores and advertisements, obstructing the view. In essence, annotations based on broadcast videos remain disconnected from the actual sensor and recording tools employed during the game, posing challenges for accurate analysis and interpretation.

## Dataset description

The dataset comprises raw-instants, which are sets of images simultaneously captured by an array of cameras, offering a panoramic view of the sports field. Specifically, it focuses solely on in-game basketball scenes. Within the DeepSport dataset, camera resolutions span from 2 megapixels (Mpx) to 5 megapixels (Mpx). Consequently, the resultant images exhibit varying levels of definition, ranging from 80 pixels per meter (px/m) to 150 px/m. This variability in image clarity is influenced by factors such as camera resolution, sensor size, lens focal length, and distance from the court.

<img src="https://github.com/dataset-ninja/deep-sport-radar/assets/120389559/a3dbcfdb-08cd-4374-80d6-25e5f265ebfb" alt="image" width="800">

<span style="font-size: smaller; font-style: italic;">A raw instant captured by the Keemotion/Synergy Automated Camera System with a two cameras setup.</span>

The dataset was captured in 15 different basketball arenas, each identified by a unique label, during 37 professional games of the French league LNB-Pro A. 

| Arena label | Arena name (City)                          | Number of items |
|-------------|--------------------------------------------|-----------------|
| ks-fr-stchamond | Halle André Boulloche (Saint-Chamond)  | 12              |
| ks-fr-fos   | HdS Parsemain (Fos-sur-Mer)               | 23              |
| ks-fr-strasbourg | Rhénus Sport (Strasbourg)              | 8               |
| ks-fr-vichy | PdS Pierre Coulon (Vichy)                | 9               |
| ks-fr-nantes | la Trocardière (Nantes)                  | 20              |
| ks-fr-bourgeb | Ekinox (Bourg-en-Bresse)                | 12              |
| ks-fr-gravelines | Sportica (Gravelines)                | 129             |
| ks-fr-monaco | Salle Gaston Médecin (Monaco)           | 9               |
| ks-fr-poitiers | Stade Poitevin (Poitiers)              | 5               |
| ks-fr-nancy | PdS Jean Weille de Gentilly (Nancy)      | 40              |
| ks-fr-lemans | Antarès (Le Mans)                       | 16              |
| ks-fr-blois | Le Jeu de Paume (Blois)                  | 39              |
| ks-fr-caen  | PdS de Caen (Caen)                       | 31              |
| ks-fr-roanne | HdS Andre Vacheresse (Roanne)           | 3               |
| ks-fr-limoges | PdS de Beaublanc (Limoges)             | 8               |

<span style="font-size: smaller; font-style: italic;">The DeepSport dataset was captured in 15 different arenas and three of them are kept for the testing set. It features a variety of angle of views, distance to the court and image resolution.</span>

The cameras employed for capturing the raw-instants are meticulously calibrated, ensuring that both intrinsic and extrinsic parameters are accurately determined. Leveraging this calibration data, the ball's 3D annotation was acquired by pinpointing two key points in the image space: the center of the ball and its corresponding vertical projection onto the ground. Annotations for human figures positioned near the court were meticulously delineated in each image, with particular attention paid to instances of occlusion, ensuring comprehensive and precise contouring.

<img src="https://github.com/dataset-ninja/deep-sport-radar/assets/120389559/c42fcde2-643c-4963-9cdf-2d98c2807e74" alt="image" width="800">

<span style="font-size: smaller; font-style: italic;">Cross section showing camera setup height from the ground and distance to the court of the different arenas in which images were acquired. The camera definition depends on camera resolution, sensor size, lens focal length and camera setup distance to the court.</span>

The dataset possesses three crucial attributes that render it highly pertinent for exploring instance segmentation in challenging scenarios. Firstly, each instance exclusively pertains to a single class. This simplifies model training and analysis by eliminating inter-class interference and the need to average performance metrics across classes with varying frequencies. Secondly, despite the singular class representation, instances exhibit diverse appearances and poses, often proving difficult to separate from the background. Additionally, occurrences of occlusion are frequent, posing formidable challenges. The high degree of interaction among instances of the same class, sometimes resulting in fragmentation into disconnected parts, places significant strain on current instance segmentation methods. Thirdly, the provided instance masks are exceedingly precise, meticulously annotated through a semi-automated process. This dataset strikes a delicate balance, offering challenges for cutting-edge models while remaining practical for research and analysis.

<img src="https://github.com/dataset-ninja/deep-sport-radar/assets/120389559/24fa060a-e2d9-4edc-ba3d-eeec5bc3d47b" alt="image" width="800">

<span style="font-size: smaller; font-style: italic;">Samples of annotated images from the instance segmentation task (cropped around annotated instances). Annotated instances are highlighted in distinct colors.</span>