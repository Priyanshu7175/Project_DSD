# Google Bigtable Infrastructure Project

## Overview
This project demonstrates the design and implementation of a distributed system using **Google Cloud Bigtable**, showcasing its low-latency, high-throughput capabilities. It explores Bigtable's seamless integration with the Hadoop ecosystem, fault tolerance, scalability, and suitability for handling large-scale data-intensive workloads. The system is designed to process real-world datasets like the **Yelp Dataset** using Google Cloud tools.

## Features
1. **Low Latency and High Throughput**:  
   Optimized for rapid response times and massive data operation handling.
2. **Data Replication and Fault Tolerance**:  
   Ensures high availability and reliability during node failures.
3. **Load Balancing**:  
   Dynamically redistributes data to handle "hot tablets" and maintain performance.
4. **Scalability**:  
   Nodes can scale horizontally to meet varying data processing demands.
5. **Seamless Ecosystem Integration**:  
   Integrates with Apache HBase and Hadoop for enhanced data processing.

## Components
- **Google Cloud Bigtable**: A scalable NoSQL database for managing structured data.
- **Google Compute Engine**: Provides virtual machines to efficiently process the data.
- **Yelp Dataset**: 9.8GB dataset simulating real-world user and business interactions.

## Dataset
The **Yelp Dataset** was used to test distributed system capabilities, focusing on performance and scalability in handling real-world data scenarios.

## System Design
- **Data Model**: Rows and column families organized with timestamps for historical data analysis.
- **Cluster Management**: Instances contain clusters distributed across multiple zones for reliability.
- **Tablet Assignment**: Data is split into tablets for distribution across nodes, enabling efficient data access.

## Team Members
- Shashwat Shah -> 40311188
- Priyanshu Adhikari -> 40262789
- Handika Harianto Ew Jong ->
- Abdulmoumen Al-Atrash -> 40180881
- Ritik Gulati ->
