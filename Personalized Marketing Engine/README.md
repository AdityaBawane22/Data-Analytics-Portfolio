Personalized Marketing Engine
Overview

The Personalized Marketing Engine is a data-driven application designed to help businesses send personalized marketing messages to their customers.
It analyzes customer data, groups customers with similar behaviors, and generates unique event-based marketing messages using artificial intelligence.
The project includes a complete dashboard that allows interaction, insights, and real-time visualization of the results.

(A) Features -
1.   Customer Segmentation:
      The system uses a clustering algorithm called DBSCAN to separate customers into distinct groups based on their purchase behavior, preferences, and patterns.
      This helps in understanding different customer types and targeting them with suitable offers.

2. Visual Generation:
      The project automatically creates visuals such as bar charts, scatter plots, and summaries to represent patterns in the data.
      These visuals help in understanding trends, purchase behavior, and customer distribution across segments.

3. Event Integration:  
    A separate event list is used to track upcoming occasions and generate greetings or promotional messages related to them.
    The event list is also used by the AI to combine relevant events with the current marketing offers for message generation.

4.   Insights Button:
    Each customer cluster includes an “Insights” button.
    When clicked, it provides quick and clear insights into that cluster, such as purchasing frequency, preferred categories, and spending behavior.

5.   Offer Selection:
    The dashboard allows selection of offers from a predefined list.
    Each offer can later be merged with current events to create relevant and timely marketing messages.

6.   AI Message Generation:
      The AI model creates personalized messages that are professional, engaging, and never repeated.

(B) Tools and Technologies - 
1.   Python:
      Used as the main programming language to build and run the application.

2.   Tkinter:
      Used to design the graphical user interface (GUI) for the dashboard, event list, and phone mockup.
      It allows users to interact with buttons, visuals, and message previews easily.

3.   Pandas:
      Used for data handling, cleaning, and manipulation.
      It reads and processes customer datasets, event lists, and offer details.

4.   Scikit-Learn:
      Used for customer segmentation through the DBSCAN algorithm.
      This library helps in clustering customers based on their purchase behavior.

5.   Matplotlib:
      Used for visual generation such as charts and graphs.
      These visuals are displayed inside the dashboard for better understanding of patterns.

6.   Ollama:
      Used for AI message generation.
      It takes the selected event, offer, and customer segment details to create unique, high-quality, and professional marketing messages.
      It combines the selected event and offer to generate unique marketing text designed for customer retention and engagement.

7.    Phone Mockup Preview:
      The phone mockup window displays a realistic preview of how the generated SMS will appear to the customer, helping visualize the final communication before         sending it.
