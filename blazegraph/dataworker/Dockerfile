FROM node:8.12.0-jessie

# Create a directory where our app will be placed
RUN mkdir /app
RUN mkdir /app/data

# Copy everything in this directory to the container
COPY ./ /app

# Copies ontologies to container
COPY ../../FRMA.rdf /app
COPY ../../HO.rdf /app
COPY ../../IMG.rdf /app
COPY ../../MLMO.rdf /app
COPY ../../PDF.rdf /app
COPY ../../Individuals.rdf /app

# Change to the app directory
WORKDIR /app
RUN npm install

# Start the dataworker
CMD ["node", "index.js"]
