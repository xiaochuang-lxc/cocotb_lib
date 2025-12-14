import xml.etree.ElementTree as ET
import argparse

def parse_xml_element(element):
    """递归解析XML元素，构建数据结构"""
    data = {
        'name': element.get('abs_name', 'unknown'),
        'size': element.get('size', 0),
        'coverage': element.get('coverage', 0),
        'cover_percentage': float(element.get('cover_percentage', 0)),
        'children': [],
        'bins': []
    }
    
    # 提取属性（weight、at_least等）
    for attr in ['weight', 'at_least']:
        if attr in element.attrib:
            data[attr] = element.get(attr)
    
    # 处理当前元素的直接子元素中的bin（不递归子元素的bin）
    for child in element:
        if child.tag.startswith('bin'):
            bin_data = {
                'name': child.get('abs_name', child.tag),
                'bin': child.get('bin', ''),
                'hits': child.get('hits', 0)
            }
            data['bins'].append(bin_data)
    
    # 处理当前元素的直接子元素（非bin），递归解析
    for child in element:
        if not child.tag.startswith('bin'):
            child_data = parse_xml_element(child)
            data['children'].append(child_data)
    
    return data

def generate_html(data):
    """递归生成HTML内容"""
    html = f'''
    <div class="coverage-item">
        <div class="item-header">
            <h2>{data['name']} (Size: {data['size']}, Covered: {data['coverage']})</h2>
            <span class="coverage-percent">{data['cover_percentage']:.2f}%</span>
        </div>
        <div class="item-content">
            <div class="coverage-bar">
                <div class="coverage-fill" style="width: {data['cover_percentage']}%"></div>
            </div>
    '''
    
    # 生成当前元素的bin列表（仅自身的bin）
    if data['bins']:
        html += '<ul class="bin-list">'
        for bin_item in data['bins']:
            html += f'''
            <li class="bin-item">
                <span class="bin-name">{bin_item['name']}: {bin_item['bin']}</span>
                <span class="bin-hits">Hits: {bin_item['hits']}</span>
            </li>
            '''
        html += '</ul>'
    
    # 递归生成子元素HTML（子折叠栏）
    if data['children']:
        html += '<div class="children-container">'
        for child in data['children']:
            html += generate_html(child)
        html += '</div>'
    
    html += '''
        </div>
    </div>
    '''
    
    return html

def xml_to_html(xml_file_path, html_file_path):
    """将XML文件转换为HTML文件"""
    # 解析XML
    tree = ET.parse(xml_file_path)
    root = tree.getroot()
    data = parse_xml_element(root)
    
    # 完整HTML模板
    full_html = f'''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Coverage Report</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            font-family: 'Arial', sans-serif;
        }}
        
        body {{
            padding: 20px;
            background-color: #f5f5f5;
        }}
        
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background-color: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
        
        h1 {{
            color: #333;
            margin-bottom: 20px;
            border-bottom: 2px solid #4CAF50;
            padding-bottom: 10px;
        }}
        
        .coverage-item {{
            margin: 15px 0;
            border: 1px solid #ddd;
            border-radius: 6px;
            overflow: hidden;
        }}
        
        .item-header {{
            padding: 12px 15px;
            background-color: #4CAF50;
            color: white;
            cursor: pointer;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}
        
        .item-header:hover {{
            background-color: #45a049;
        }}
        
        .item-header h2 {{
            font-size: 18px;
            font-weight: normal;
        }}
        
        .coverage-percent {{
            font-weight: bold;
            background-color: rgba(255,255,255,0.2);
            padding: 4px 8px;
            border-radius: 4px;
        }}
        
        .item-content {{
            padding: 15px;
            display: none;
            background-color: #f9f9f9;
        }}
        
        .bin-list {{
            list-style-type: none;
            margin-top: 10px;
            margin-bottom: 15px;
        }}
        
        .bin-item {{
            padding: 8px 10px;
            border-bottom: 1px solid #eee;
            display: flex;
            justify-content: space-between;
        }}
        
        .bin-item:last-child {{
            border-bottom: none;
        }}
        
        .bin-name {{
            font-weight: 500;
            color: #555;
        }}
        
        .bin-hits {{
            color: #2196F3;
            font-weight: bold;
        }}
        
        .children-container {{
            margin-left: 20px;
            margin-top: 15px;
        }}
        
        .coverage-bar {{
            height: 8px;
            background-color: #e0e0e0;
            border-radius: 4px;
            margin-top: 5px;
            overflow: hidden;
        }}
        
        .coverage-fill {{
            height: 100%;
            background-color: #4CAF50;
            border-radius: 4px;
            transition: width 0.3s ease;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>Coverage Report</h1>
        <div id="coverage-content">
            {generate_html(data)}
        </div>
    </div>
    <script>
        // 折叠/展开功能
        document.addEventListener('DOMContentLoaded', function() {{
            const headers = document.querySelectorAll('.item-header');
            headers.forEach(header => {{
                header.addEventListener('click', function() {{
                    const content = this.nextElementSibling;
                    content.style.display = content.style.display === 'block' ? 'none' : 'block';
                }});
            }});
        }});
    </script>
</body>
</html>
    '''
    
    # 写入HTML文件
    with open(html_file_path, 'w', encoding='utf-8') as f:
        f.write(full_html)
    
    print(f"成功生成HTML文件: {html_file_path}")

if __name__ == "__main__":
    # 命令行参数解析
    parser = argparse.ArgumentParser(description='将覆盖率XML文件转换为HTML文件')
    parser.add_argument('xml_file', help='输入的XML文件路径')
    parser.add_argument('html_file', help='输出的HTML文件路径')
    args = parser.parse_args()
    
    # 执行转换
    xml_to_html(args.xml_file, args.html_file)