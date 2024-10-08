TO DO: </br>
-Video 90s</br>
-Files on Design. Can probably be code.</br>
-A Jupyter Notebook.</br>
-A Readme File for the finished thing. (Just edit this and delete all these at the end).</br></br>

# GreenThumBot - Greening Belfast for a Sustainable Future

## Overview

GreenThumBot is an innovative project focused on enhancing urban green spaces, increasing tree coverage, and promoting sustainable practices to protect Belfast's environment and helping every day people get involved with improving the world around them. It leverages data from OpenData NI datasets such as the Belfast Trees Dataset, Belfast City Parks, and Areas of Outstanding Beauty to identify optimal locations for tree planting and green infrastructure development.

Our challenge is simple yet impactful: How can we harness technology, data, and community involvement to create a greener Belfast? GreenThumBot is our solution, combining technology, data, and community spirit to transform Belfast's urban landscape.

## Current Functionality

The project consists of two main components:

**Backend (Flask Server)**: Located in the hackathon-backend repository, this Python Flask server provides the necessary functionality to analyze datasets from OpenData NI. It generates maps of Belfast displaying current tree locations, pollution levels, and recommended areas for new tree planting initiatives. The Flask server offers an API that communicates with the frontend to provide map data and analysis results.

**Frontend (Angular Application)**: The frontend, located in the [hackathon-frontend](https://github.com/ireleezi/hackathon-frontend) repository, allows users to interact with the backend data. Users can view maps and gain insights into current tree coverage, pollution levels, and community planting opportunities. The UI is designed to be simple yet informative, providing a clear view of urban greening initiatives.

To run the project, simply start the Flask server by running python app.py in the backend repository and manually boot up the Angular server using ng serve in the frontend repository. Both components run on localhost:4200 and are currently not containerized.

## Current Features

- Tree Location Analysis: Visualize the existing tree coverage across Belfast.

- Pollution Mapping: Identify areas with higher pollution levels where tree planting could help mitigate effects.

- Planting Recommendations: Suggest optimal planting locations based on tree density and pollution data.


## Future Functionality

We envision expanding GreenThumBot into two distinct versions to address both community and industrial needs:

**Community Version**: Aimed at local residents, this version will allow users to: 
- View community gardens and green spaces
- Adopt and monitor trees trees
- Register plots in the app to monitor
- Recieve recommendations and crucial information on any registered plants fed to them in real-time via any GreenThumBot units

**Industrial Version**: This version will cater to local councils, environmental agencies, and large organizations. It will provide:
- A city-wide overview, including information on tree numbers, planting sites, pollution levels, and more.
- This version will help in making strategic decisions for urban planning and sustainability initiatives.

## Advanced Machine Learning and IoT Integration

The analysis will be further developed using a more advanced machine learning model that takes into consideration a wider range of variables, including:

- Buildings and infrastructure (e.g., roads, urban development zones).

- Planning permissions for different sites.

- Availability of resources for planting.

- Proximity of people to recommended planting sites.

- This enriched model will provide more sophisticated recommendations, enhancing the accuracy and impact of our greening initiatives.

The GreenThumBot hardware unit will also undergo significant improvements. Currently, the prototype measures soil humidity, pH levels, and uses a basic camera to monitor individual plant growth at registered sites. In future iterations, the unit will incorporate more advanced sensors and data analytics, allowing for better monitoring and actionable insights for users.

## Expanding the User Interface

The UI will be developed further to provide a more seamless user experience, facilitating:

Real-time Notifications: Updates on plant health, recommendations for care, and upcoming community events.

Interactive GIS Mapping: Detailed maps for understanding local ecosystems, green roofs, rain gardens, and other nature-based solutions.

Community Dashboard: Insights into local green spaces, community activities, and a space for users to share their progress and success stories.

## Key Goals for the Future

**Increase Tree Coverage**: By analyzing soil conditions and urban infrastructure, we suggest the best places to plant new trees. Users can join community planting events, adopt a tree, and track its growth with real-time updates.

**Protect Local Ecosystems**: IoT sensors through GreenThumBot units will monitor the health of green spaces, providing data that helps in preserving and restoring natural habitats.

**Promote Nature-Based Solutions**: Implement green roofs, rain gardens, and other solutions where they will make the biggest impact.

**Embed Sustainable Food Practices**: Participate in community gardens that provide fresh produce and support local wildlife.

**Deploy GreenThumBot units**: The physical GreenThumBot hardware will be able to give us more insights on improving Belfast and improve community participation as even the average joe can learn how to garden.

## Generative AI Integration

During the hackathon, we utilized generative AI tools like ChatGPT for idea generation, data modeling, and solution refinement. This allowed us to process large datasets efficiently and develop predictive models for tree planting and ecosystem management. By integrating generative AI, we accelerated our development process and created a more effective, user-friendly platform.

## Containerization Next Steps

To further enhance the deployment process and make the project more scalable, we plan to containerize both the backend and frontend components using Docker. Containerization will enable easier setup, consistent environments, and better resource management. The next steps for containerization are as follows:

Create Dockerfiles: Develop Dockerfiles for both the backend (Flask server) and the frontend (Angular application).



Backend Dockerfile: Set up a Python environment with necessary dependencies, expose the required port, and run the Flask server.

- **Frontend Dockerfile**: Set up a Node environment, install Angular dependencies, and serve the application.

Docker Compose Setup: Create a docker-compose.yml file:



Testing and Debugging: Test the containerized environment locally to ensure both services work well together in isolated containers. Debug any issues related to networking or dependency conflicts.

Deployment: Once containerized, deploy the services using a container orchestration platform like Kubernetes or use cloud services such as AWS, Azure, or Google Cloud to manage the deployment and scaling of the containers.

CI/CD Integration: Integrate the containerization process into a CI/CD pipeline. This will automate building, testing, and deploying the containers, ensuring a streamlined workflow for further development.

Join Us in Greening Belfast

Together, we can create a sustainable future for Belfast. GreenThumBot is designed to empower both the community and local authorities to take action towards increasing tree coverage, protecting green spaces, and promoting sustainable urban practices. With GreenThumBot, small actions can lead to big changes. Let's make Belfast greener, healthier, and more sustainable for generations to come.



</br>
</br>
<img src="testing.jpg" alt="O'Brien" width="2000"/>
