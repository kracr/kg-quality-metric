# #!/bin/bash

# # Run Python script
# python3 Triple_Extractor.py

# # Compile Java code
# javac -cp .:json-simple-1.1.1.jar Main.java

# # Run Java program
# java -cp .:json-simple-1.1.1.jar Main


#!/bin/bash

# Step 1: Run Python extractor
# python3 Triple_Extractor.py

# Step 2: Compile Java with all dependencies
javac -cp ".:json-simple-1.1.1.jar:commons-text-1.10.0.jar:commons-lang3-3.12.0.jar" Main.java

# Step 3: Run Java
java -cp ".:json-simple-1.1.1.jar:commons-text-1.10.0.jar:commons-lang3-3.12.0.jar" Main
