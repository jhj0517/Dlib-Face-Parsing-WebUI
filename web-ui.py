# Copyright [2023] [jhj0517]

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import gradio as gr
from tkinter import filedialog, Tk
import os
from parse import parse

def generate_output(input_path,output_path):
    try:
        parse(input_path=input_path,output_path=output_path)
        return gr.Markdown.update("<center><h5>Completed!</h5></center>")
    except Exception as e:
        return gr.Markdown.update(f"<center>Error Occured!<br>{e}</center>")    

def get_file_path(file_path=''):

    initial_dir, initial_file = os.path.split(file_path)

    root = Tk()
    root.wm_attributes('-topmost', 1)
    root.withdraw()
    file_path = filedialog.askopenfilename(
        initialdir=initial_dir,
        initialfile=initial_file,
    )
    root.destroy()

    return file_path

def get_folder_path(folder_path=''):

    initial_dir, initial_file = os.path.split(folder_path)

    root = Tk()
    root.wm_attributes('-topmost', 1)
    root.withdraw()
    folder_path = filedialog.askdirectory(initialdir=initial_dir)
    root.destroy()
    
    return folder_path

def app():
    css="""
    #btn_file {height: auto; min-width: auto; flex-grow: 0; padding-left: 2em; padding-right: 2em;}
    #btn_folder {height: auto; min-width: auto; flex-grow: 0; padding-left: 2em; padding-right: 2em;}
    #component-3 {max-width: 60%; margin: 0 auto;}
    #component-7 {max-width: 60%; margin: 0 auto;}
    #component-11 {max-width: 20%; min-height: 200%; margin: 0 auto;}
    """

    interface = gr.Blocks(css=css)
    with interface:
        with gr.Tab("Dlib-Face Parsing WEB-UI"):
                gr.Markdown(
                    """
                    <p align="center" style="font-size: 17px;">
                    For the latest updates on this , please visit <a href="https://github.com/jhj0517/Dlib-Face-Parsing-WebUI">here</a><br>
                    <img src="https://raw.githubusercontent.com/jhj0517/Dlib-Face-Parsing-WebUI/master/example/example.png" alt="" width="40%">
                    If you found this project useful, please consider supporting it by buying me a coffee. <br>
                    <a href="https://www.buymeacoffee.com/jhj0517" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/default-orange.png" alt="Buy Me A Coffee" height="41" width="174"></a>
                    </p>
                    """
                )
                with gr.Row():
                    tb_input_path = gr.Textbox(
                        label='Enter the path for input image',
                        placeholder='enter the path for input image',
                        elem_id="tb_file",
                        interactive=True
                    ) 
                    btn_file = gr.Button(
                        '🖼️', elem_id='btn_file'
                    )
                    btn_file.click(
                        get_file_path,
                        inputs=tb_input_path,
                        outputs=tb_input_path,
                    )
                with gr.Row():
                    tb_output_path = gr.Textbox(
                        label='Enter the output folder path',
                        placeholder='Enter the folder where the results will be saved',
                        elem_id="tb_folder",
                        interactive=True
                    )
                    btn_folder = gr.Button(
                        '📂', elem_id='btn_folder'
                    )
                    btn_folder.click(
                        get_folder_path,
                        inputs=tb_output_path,
                        outputs=tb_output_path,
                    )
                with gr.Row():
                    btn_run = gr.Button(
                        'RUN', elem_id='generate'
                    )
                md_indic = gr.Markdown('<center><h5></h5></center>')
    
        btn_run.click(
            fn=generate_output,
            inputs =[tb_input_path,tb_output_path],
            outputs=[md_indic]
        )                               

    interface.launch()

if __name__ == '__main__':
    app()