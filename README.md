https://github.com/MichelCats36/COD-WW2-Texture-Loader/


# COD-WW2-Texture-Loader
The "Texture Loader Add-on" is a powerful tool designed for Blender, specifically aimed at helping you manage materials and textures in your 3D projects. If you're working on complex scenes with lots of materials and textures—like game assets, architectural models, or detailed environments—this add-on can save you a lot of time and hassle.

# Key Features:
Import Material Names: Easily load material names from a JSON file directly into Blender.
Rename Files: Clean up your file names by removing unwanted suffixes or special characters.
Load Textures Automatically: Select directories for your textures and texture information files, and let the add-on handle the rest. It will create and assign materials to your meshes based on the files you provide.
Cleanup and Replace Materials: Automatically clean up duplicated materials and textures, ensuring your scene stays organized and optimized.
Mapping Materials to Textures and Meshes: Get a clear overview of which materials use which textures, and which meshes they are applied to.

# How to Use the Add-on:
Installation:

Save the script as a .py file.
In Blender, go to Edit > Preferences > Add-ons > Install..., and select the script.
Enable the add-on from the list.
Setup:

Once enabled, you’ll find a new panel called "Texture Loader" in the 3D View under the View tab.
Start by selecting your directories using the buttons for Select Texture Info Directory and Select Texture Directory. These are the folders where your texture information files and actual texture files are stored.
Using the Functions:

Load Material Names: If you have a JSON file with material names, use the Get Material Names from JSON button to load them into Blender.
Rename Files: Use the Rename Files and Rename Special Characters buttons to clean up any unwanted file names or characters in your directories.
Load Textures: Once your directories are set, click Load Textures to automatically load and apply textures to your materials and meshes.
Cleanup and Replace: After loading, use the Cleanup and Replace button to tidy up your scene, removing any unused materials or textures.
Mapping: If you want to see how materials, textures, and meshes are connected, use the Material Texture Mesh Mapping button to create a detailed mapping in Blender’s text editor.

# Why Use It?
If you’re dealing with large projects that involve many textures and materials, this add-on simplifies the process of organizing, applying, and cleaning up your assets. It reduces the manual work and ensures that your materials are correctly applied and managed within Blender.

# Required Programs
To use this add-on effectively, you will need the following external programs, which are included in the zip file:


# Grayhound

Description: Grayhound is a powerful tool used for extracting and managing assets.
Download Link: Grayhound on GitHub
Credits: Developed by Scobalula.


# C2M v1

Description: C2M v1 is used for converting and managing texture files.
Download Link: C2M v1 on GitHub
Credits: Developed by sheilan102, updated and maintained by vugi99.


# C2M v2

Description: C2M v2 is the latest version of the C2M tool, offering additional features and improvements.
Download Link: C2M v2 on GitHub
Credits: Developed by sheilan102.


# Credits/Contributors
We would like to thank the developers of these tools for their invaluable contributions.




# Detailed Breakdown of the Script:
1. Add-on Metadata and Registration
bl_info: This dictionary provides metadata about the add-on, including its name, the Blender version it’s compatible with, and its category. This information is used by Blender to display and manage the add-on in the preferences menu.
register/unregister functions: These functions handle the registration and unregistration of the add-on’s classes. When the add-on is enabled or disabled in Blender, these functions are automatically called to set up or tear down the add-on.
2. Operators
Operators in Blender are reusable blocks of functionality that can be triggered by the user. This script defines several custom operators, each serving a specific purpose related to material and texture management.

MATERIAL_OT_get_names_from_json:

Purpose: This operator allows users to import material names from a JSON file into Blender's text editor. It reads the JSON file, extracts the material names, and writes them to a new text block in Blender.
How it works:
The JSON file is selected using Blender’s file browser.
The operator checks if the file exists, loads the JSON data, extracts the material names, and writes them into a new text block in Blender’s scripting tab.
Use case: This is useful when you have a predefined set of material names in a JSON format, and you want to quickly import them into Blender for reference or further processing.
MATERIAL_OT_rename_files:

Purpose: This operator renames .txt and .mtl files within a specified directory by removing a specific suffix (_images).
How it works:
The user selects the root directory.
The operator iterates through all files in the directory and its subdirectories, identifies files with the specified suffix, and renames them by removing the suffix.
Use case: This is helpful when managing large sets of texture files that have been exported with consistent but unnecessary suffixes, which you want to remove for cleaner file names.
MATERIAL_OT_rename_special_characters:

Purpose: This operator replaces special characters (~, &, $) in .txt and .mtl files with underscores.
How it works:
Similar to the previous operator, the user selects a directory.
The operator reads each file, replaces the special characters in the content, and writes the modified content back to the file.
Use case: This is particularly useful for cleaning up file content to ensure compatibility with different systems or software that might not handle special characters well.
MATERIAL_OT_rename_textures_files:

Purpose: This operator is similar to MATERIAL_OT_rename_special_characters, but it operates on texture files (e.g., .png, .jpg, etc.) and renames them by replacing special characters in their filenames.
How it works:
The operator scans the directory, identifies texture files, and renames them by replacing specified special characters with underscores.
Use case: This is useful when your texture files contain special characters that you need to remove for better organization or compatibility reasons.
MATERIAL_OT_cleanup_and_replace:

Purpose: This operator performs a comprehensive cleanup of material and texture names within Blender, replaces materials in meshes, and removes unused materials and textures.
How it works:
Cleanup names: It iterates through materials and textures, normalizing their names by removing unwanted suffixes (e.g., .001), which often appear when duplicating materials or textures in Blender.
Replace materials in meshes: It then updates the meshes to use the cleaned-up material names.
Replace textures in materials: Similarly, it updates the texture nodes within materials to use the cleaned-up texture names.
Remove unused materials and textures: Finally, it removes any materials or textures that are no longer used by any objects in the scene.
Use case: This operator is ideal for optimizing and cleaning up a Blender project, particularly after importing or duplicating assets that may have created redundant or poorly named materials and textures.
MATERIAL_OT_mapping:

Purpose: This operator creates a mapping of materials to the textures they use and the meshes they are applied to. It writes this mapping to a new text block in Blender.
How it works:
The operator iterates through all materials, identifying the textures used by each material.
It also identifies the meshes that each material is assigned to.
The results are written to a text block for easy review and reference.
Use case: This is useful for auditing a scene, allowing you to see at a glance which materials are using which textures and where they are applied, helping to manage complex scenes with many assets.
TEXTURE_OT_select_texture_info_directory & TEXTURE_OT_select_texture_directory:

Purpose: These two operators allow the user to select directories within Blender that will be used later for loading textures.
How it works:
The user is prompted to select directories via the file browser.
The selected paths are stored in the Blender scene context for use by other operators.
Use case: These operators prepare the necessary information for texture loading operations, ensuring that the correct directories are used.
TEXTURE_OT_load_textures:

Purpose: This operator loads textures into Blender, creates materials, and assigns them to the appropriate meshes based on the previously selected directories.
How it works:
It searches the selected directories for texture files and information files (e.g., .txt, .mtl).
For each texture information file, it reads the file to determine how textures should be applied to materials.
It creates or updates materials in Blender using these textures, setting up nodes appropriately (e.g., connecting diffuse maps, normal maps, etc.).
It then assigns these materials to meshes that match the material names.
Use case: This operator is crucial for automating the process of setting up materials in Blender, especially in workflows where materials and textures are defined externally and need to be quickly and accurately applied to 3D models.
3. Helper Functions
collect_base_materials, assign_materials_to_objects, assign_missing_materials, assign_base_material_to_duplicates:
Purpose: These functions help manage the assignment of base materials to objects, ensuring that duplicated objects in Blender use consistent materials.
How it works:
They first collect all base materials (original versions of duplicated materials).
Then, they assign these base materials to objects, ensuring consistency across the scene.
Use case: These functions are particularly useful in large projects where objects may have been duplicated multiple times, leading to cluttered material lists with unnecessary duplicates.
4. Panel and UI Integration
TEXTURE_PT_panel:
Purpose: This panel adds a user interface to Blender’s 3D view, under the "Texture Loader" tab, providing a convenient place to access all the operators defined in the script.
How it works:
The panel is placed in Blender’s UI and contains buttons for each operator, allowing users to run these operations directly from the 3D view.
Use case: This UI integration makes the add-on user-friendly, providing easy access to its functionality without needing to run scripts manually or dig through menus.
5. Menu Integration
menu_func:
Purpose: This function adds entries to Blender’s import menu, allowing some of the operators to be accessed from the file menu.
How it works:
When the add-on is registered, this function appends the necessary operators to the file import menu, providing another way for users to access the add-on’s functionality.
Use case: It provides additional accessibility, integrating the add-on’s features into Blender’s existing menu structure.
Summary of Usage:
Installation and Activation:

Install the script as a Blender add-on.
Enable it in the Blender preferences.
Workflow:

Start by using the operators in the "Texture Loader" panel to set up directories and load material names if needed.
Use the rename operators to clean up file names and content in your directories.
Load textures and apply them to your meshes automatically using the TEXTURE_OT_load_textures operator.
Perform final cleanups and material replacements using the MATERIAL_OT_cleanup_and_replace operator.
Review the material-to-texture mappings generated by the MATERIAL_OT_mapping operator.
By following these steps, you can efficiently manage and apply textures and materials in Blender, especially in projects involving a large number of assets or complex material setups. This script is particularly valuable for game developers, VFX artists, and anyone working with imported assets where manual material setup would be time-consuming and error-prone.

