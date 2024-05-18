docker build -t e-commerce-flask .  # Create an image


docker run -d -p 5000:5000 -w /app -v "$(pwd):/app" flask-e-commerce  # Run the container

-w = current working directory of the conatiner
-v = linking the pwd(host) to the work directory of the container
