import argparse
from urllib.parse import urlparse

def normalize_url(url):
    """标准化URL以便更好地去重"""
    # 去除首尾空白字符
    url = url.strip()
    
    # 尝试解析URL
    try:
        parsed = urlparse(url)
        
        # 标准化：小写化域名，移除默认端口，标准化路径等
        netloc = parsed.netloc.lower()
        if ':' in netloc:
            host, port = netloc.split(':', 1)
            # 移除HTTP默认端口80和HTTPS默认端口443
            if port == '80' and parsed.scheme == 'http':
                netloc = host
            elif port == '443' and parsed.scheme == 'https':
                netloc = host
        
        # 重建标准化URL
        normalized = parsed._replace(netloc=netloc, path=parsed.path.rstrip('/'))
        return normalized.geturl()
    except:
        # 如果无法解析，返回原始URL（去除首尾空白）
        return url

def remove_duplicate_urls(input_file, output_file=None):
    """从输入文件中读取URL并去重"""
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            urls = f.readlines()
    except FileNotFoundError:
        print(f"错误：文件 '{input_file}' 未找到")
        return
    except Exception as e:
        print(f"读取文件时出错: {e}")
        return
    
    # 去重处理
    unique_urls = set()
    for url in urls:
        if url.strip():  # 跳过空行
            normalized = normalize_url(url)
            unique_urls.add(normalized)
    
    # 输出到文件或控制台
    if output_file:
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                for url in sorted(unique_urls):
                    f.write(url + '\n')
            print(f"去重完成！原始URL数量: {len(urls)}，去重后数量: {len(unique_urls)}")
            print(f"结果已保存到: {output_file}")
        except Exception as e:
            print(f"写入输出文件时出错: {e}")
    else:
        # 输出到控制台
        for url in sorted(unique_urls):
            print(url)
        print(f"\n去重完成！原始URL数量: {len(urls)}，去重后数量: {len(unique_urls)}")

def main():
    parser = argparse.ArgumentParser(description='URL去重工具')
    parser.add_argument('-l', '--list', dest='input_file', required=True,
                        help='包含URL列表的输入文件')
    parser.add_argument('-o', '--output', dest='output_file',
                        help='输出文件（可选），如果不指定则输出到控制台')
    
    args = parser.parse_args()
    
    remove_duplicate_urls(args.input_file, args.output_file)

if __name__ == '__main__':
    main()