'''
该文件用于存放一些将数据保存到文件的方法

writeNiigz: 将数据保存到nii.gz文件
writePdf: 将数据保存到pdf文件
'''


import os

def writeNiigz(data, output):
    '''
    保存文件
    '''
    import SimpleITK as sitk
    sitk.WriteImage(data, output)
    pass

def writePdf(data, output):
    output = os.path.abspath(output)
    data.SaveAs(output, FileFormat=32)
    data.Close()
    pass
