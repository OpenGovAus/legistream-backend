'''
                                    .,.                                        
                               @@(#@    @                                       
                               @    @%/@@                                       
                                        @                                       
                                        @                                       
                                      #,@ @                                     
                                    %,#@@@@ @                                   
                                    %,#,@ @ @                                   
                                    %,#,@ @ @                                   
                                    &,#&@&@ @                                   
                                 #@  @*    @* /@                                
                              @#  @,          @( .@.                            
                       ,###@@##@&####      ,#####@%##@###.                      
     OpenGov Australia*#*@.../(     @@@  *@@/     @....%@/*****************.    
     @,#,,,& %,,,% %,,,% @   *(       @  *(       @    %@*,,,@@*,,,@/(...&,/    
     @,/   % #   # #   # @   *(       @((#(       @    %@.   @@.   @/*   &,/    
     @,/   % #   # #   # @   *(%&&&&&/&&&&&,&&&&&.@    %@.   @@.   @/*   &,/    
     @,/   % #   # #   # @   *(&    @/,   @*(   @.@    %@.   @@.   @/*   &,/    
     @,/   % #   # #   # @   *(&    @/,   @*(   @.@    %@.   @@.   @/*   &,/    
     @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@/
'''

from setuptools import setup, find_packages
import pathlib

here = pathlib.Path(__file__).parent.resolve()

long_description = (here / 'README.md').read_text(encoding='utf-8')

setup(
    name='legistream-backend',
    version='1.0.2',
    description='Get live stream metadata from the various Australian parliaments.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/OpenGovAus/legistream-backend',
    author='king-millez',
    author_email='millez.dev@gmail.com',
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
    packages=find_packages(),
    python_requires='>=3.6'
)