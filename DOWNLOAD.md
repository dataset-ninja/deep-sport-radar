Dataset **DeepSportRadar** can be downloaded in [Supervisely format](https://developer.supervisely.com/api-references/supervisely-annotation-json-format):

 [Download](https://assets.supervisely.com/remote/eyJsaW5rIjogImZzOi8vYXNzZXRzLzM1ODlfRGVlcFNwb3J0UmFkYXIvZGVlcHNwb3J0cmFkYXItRGF0YXNldE5pbmphLnRhciIsICJzaWciOiAiK3FNR0VZVUpNTGdvU2J0QWgzcTM5bGlGUytZc2NjNXFObmhla1JRbGlMUT0ifQ==)

As an alternative, it can be downloaded with *dataset-tools* package:
``` bash
pip install --upgrade dataset-tools
```

... using following python code:
``` python
import dataset_tools as dtools

dtools.download(dataset='DeepSportRadar', dst_dir='~/dataset-ninja/')
```
Make sure not to overlook the [python code example](https://developer.supervisely.com/getting-started/python-sdk-tutorials/iterate-over-a-local-project) available on the Supervisely Developer Portal. It will give you a clear idea of how to effortlessly work with the downloaded dataset.

The data in original format can be [downloaded here](https://www.kaggle.com/datasets/deepsportradar/basketball-instants-dataset/download?datasetVersionNumber=4).