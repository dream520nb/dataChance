'''
该文件用于存放一些将数据保存到文件的方法

writeNiigz: 将数据保存到nii.gz文件
writePdf: 将数据保存到pdf文件
'''


def writeNiigz(data, output):
    '''
    保存文件
    '''
    import SimpleITK as sitk
    sitk.WriteImage(data, output)
    pass

def writePdf(data, output):
    import pdfkit
    presentation = data
    # 暂存每一张幻灯片的内容
    html_content = ''
    for slide_index, slide in enumerate(presentation.slides):
        html_content += f'<h1>Slide {slide_index + 1}</h1>'
        
        for shape in slide.shapes:
            if hasattr(shape, "text"):
                html_content += f'<p>{shape.text}</p>'
    
    # 保存为 HTML 文件
    html_file_path = 'temp_slide.html'
    with open(html_file_path, 'w', encoding='utf-8') as f:
        f.write(html_content)

    # 使用 pdfkit 将 HTML 转换为 PDF
    pdfkit.from_file(html_file_path, output)
    pass
