'''
Function:
    setup the pytools
Author:
    Charles
微信公众号:
    Charles的皮卡丘
GitHub:
    https://github.com/CharlesPikachu
'''
import pytools
from setuptools import setup, find_packages


'''readme'''
with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()


'''package data'''
package_data = {}
package_data.update({
    'pytools.modules.runcat': ['resources/*'] 
})
package_data.update({
    'pytools.modules.ukrainemap': ['resources/*', 'icon.png'] 
})
package_data.update({
    'pytools.modules.desktoppet': ['resources/bingdwendwen/*', 'resources/blackcat/*', 'resources/fox/*', 'resources/pikachu/*', 'resources/whitecat/*'] 
})
package_data.update({
    'pytools.modules.translator': ['resources/*'] 
})
package_data.update({
    'pytools.modules.videoplayer': ['resources/*'] 
})
package_data.update({
    'pytools.modules.musicplayer': ['resources/*'] 
})
package_data.update({
    'pytools.modules.idcardquery': ['resources/*'] 
})
package_data.update({
    'pytools.modules.playfireworks': ['resources/*'] 
})
package_data.update({
    'pytools.modules.computersinger': ['resources/icon.ico', 'resources/musicfiles/*'] 
})
package_data.update({
    'pytools.modules.inquiryexpress': ['resources/*'] 
})
package_data.update({
    'pytools.modules.idiomsolitaire': ['resources/*'] 
})
package_data.update({
    'pytools.modules.genderpredictor': ['resources/*'] 
})
package_data.update({
    'pytools.modules.succulentquery': ['resources/icon.png', 'resources/succulents/AK/*'] 
})
package_data.update({
    'pytools.modules.qrcodegenerator': ['resources/*'] 
})
package_data.update({
    'pytools.modules.coupletgenerator': ['resources/*'] 
})
package_data.update({
    'pytools.modules.artsigngenerator': ['resources/*'] 
})
package_data.update({
    'pytools.modules.controlpcbyemail': ['resources/*'] 
})
package_data.update({
    'pytools.modules.naughtyconfession': ['resources/music/*', 'resources/font/*', 'resources/images/*'] 
})
package_data.update({
    'pytools.modules.luxunsentencesquery': ['resources/*'] 
})
package_data.update({
    'pytools.modules.hubbleseeonbirthday': ['resources/hubble-birthdays-full-year.xlsx', 'resources/icon/*'] 
})
package_data.update({
    'pytools.modules.newyearcardgenerator': ['resources/bgimages/*', 'resources/contents/*', 'resources/fonts/*', 'resources/icon/*'] 
})
package_data.update({
    'pytools.modules.trumptweetsgenerator': ['resources/*'] 
})
package_data.update({
    'pytools.modules.sovietgenerator': ['resources/*'] 
})
package_data.update({
    'pytools.modules.goodgoodgenerator': ['resources/*'] 
})
package_data.update({
    'pytools.modules.tianyancha': ['resources/*'] 
})


'''setup'''
setup(
    name=pytools.__title__,
    version=pytools.__version__,
    description=pytools.__description__,
    long_description=long_description,
    long_description_content_type='text/markdown',
    classifiers=[
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 3',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent'
    ],
    author=pytools.__author__,
    url=pytools.__url__,
    author_email=pytools.__email__,
    license=pytools.__license__,
    include_package_data=True,
    package_data=package_data,
    install_requires=[lab.strip('\n') for lab in list(open('requirements.txt', 'r').readlines())],
    zip_safe=True,
    packages=find_packages(),
)