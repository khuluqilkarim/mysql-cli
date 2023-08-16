import pyfiglet

# Text for the banner
banner_text = """
      ___      ___         ___      ___         ___ 
     /\__\    |\__\       /\  \    /\  \       /\__\\\n
    /::|  |   |:|  |     /::\  \  /::\  \     /:/  /\n
   /:|:|  |   |:|  |    /:/\ \  \/:/\:\  \   /:/  / \n
  /:/|:|__|__ |:|__|__ _\:\~\ \  \:\~\:\  \ /:/  /  \n
 /:/ |::::\__\/::::\__/\ \:\ \ \__\:\ \:\__/:/__/   \n
 \/__/~~/:/  /:/~~/~  \:\ \:\ \/__/\:\/:/  \:\  \   \n
       /:/  /:/  /     \:\ \:\__\   \::/  / \:\  \  \n
      /:/  /\/__/       \:\/:/  /   /:/  /   \:\  \ \n
     /:/  /              \::/  /   /:/  /     \:\__\\\n
     \/__/                \/__/    \/__/       \/__/\n
"""

# Generate the ASCII art with smaller font size
ascii_banner = pyfiglet.figlet_format(banner_text, font='small')

# Print the banner
print(ascii_banner)
