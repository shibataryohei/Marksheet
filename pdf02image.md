# 0. はじめに
スキャナで取り込む時はどうやら`.pdf`か`.jpg`となってしまうようなので、PDFをPNGに変換する必要があります。

# 1. 
```bash
pip install pdf2image --user
pip install pillow --user
brew install poppler
```
 
```python
from pdf2image import convert_from_path

path = 'PDFを置いてる場所'
images = convert_from_path(path)

i = 0
for image in images:
    image.save('test{}.png'.format(i), 'png')
    i += 1
```