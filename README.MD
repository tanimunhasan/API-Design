# NB-IoT Sensor API using FastAPI

This project is a Python FastAPI backend for receiving, storing, and retrieving NB-IoT sensor data.

The API was developed as part of an NB-IoT/UDP-to-cloud learning project. The system can receive incoming sensor payloads, save them into a SQLite database, and expose useful API endpoints for history, filtering, searching, and device listing.

---

## Project Purpose

The main purpose of this project is to learn and build a REST API backend that can be used with IoT devices, cloud servers, databases, dashboards, and frontend applications.

The current API supports:

- Receiving NB-IoT payload data
- Saving data into SQLite
- Reading the latest packet
- Reading packet history
- Searching packets by payload keyword
- Filtering packets by source IP
- Reading one packet by ID
- Listing unique devices/source IPs

---

## System Flow

```text
NB-IoT Device / UDP Bridge
        ↓
FastAPI Backend
        ↓
SQLite Database
        ↓
Frontend / Dashboard / API Client