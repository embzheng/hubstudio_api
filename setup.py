import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()   

project_urls = {
  'Source': 'https://github.com/embzheng/hubstudio_api'
}

setuptools.setup(
    name="hubstudio_api",
    version="0.1",
    author="embzheng",
    author_email="embzheng@qq.com",
    description="This is a log tool",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/embzheng/hubstudio_api",
    packages=setuptools.find_packages(),
    install_requires=['my_logtool','requests','playwright','subprocess','json','time'],    
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    project_urls = project_urls
)