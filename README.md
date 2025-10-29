# Overview

“Crowd prediction as the core, alternative recommendations as support.”
Taiwan’s first Line-based scenic spot crowd prediction platform

## Key Features

24-hour crowd forecast (updated every 15 minutes)

Risk Index: integrates crowd density (%), rainfall probability, and perceived temperature

Top 5 nearby alternative attractions recommended

Attraction stories: promoting local culture and heritage

Real-time weather information: perceived temperature, humidity, and rainfall probability

## How to Use

Add the Line Bot as a friend → enter a destination or enable location → instantly receive detailed information.
Supports two modes:

Specific destination search

Nearby attractions inquiry

# Technical Highlights (MVC Architecture + Cloud Deployment)

| Item | Technical Details |
| :--- | :--- |
| **Frontend** | Line Flex Message + Regex command recognition |
| **Backend** | Python + Flask |
| **Data Sources** | - Taipei City Tourism Bureau API (attraction stories, latitude/longitude)<br>- Central Weather Bureau API (weather, perceived temperature)<br>- Google Geocoding API (place name to latitude/longitude) |
| **Crowd Flow Prediction Model** | 1. Classify attractions into 7 types (night markets, old streets, cultural venues, etc.)<br>2. Collect Google Popular Times data for 30–50 attractions per type<br>3. Average Saturday/Sunday data → 6th-degree polynomial regression (MATLAB)<br>4. Generate "time vs. crowd percentage" function |
| **Cloud Deployment** | Heroku (free Dyno + 1GB Postgres) |

<img width="813" height="330" alt="image" src="https://github.com/user-attachments/assets/89c912a0-e1dd-4008-b9bd-51965f013f48" />



# Market Positioning and Business Model

## Target Market
| Aspect                  | Description                                                                 |
|-------------------------|-----------------------------------------------------------------------------|
| **Main Market**         | Taipei and New Taipei City (雙北)                                           |
| **Target Age Group**    | 12-55 years old                                                            |
| **Key Behaviors**       | Want to avoid crowds, use LINE app, pedestrian/scooter users                |
| **Potential Customer Base** | Approximately 3.678 million people (population aged 12-55 in Taipei-New Taipei) |
| **Brand Positioning**   | "Enable young professionals in Taipei-New Taipei to quickly check crowd flow and avoid crowds" |

## Business Model
| Income Source | Description |
| :--- | :--- |
| **Annual Fee for New Startup Stores** | Priority recommendation (algorithm push) for new startup stores. |
| **Advertising Space** | Advertising placement by legitimate stores. |
| **Government Cooperation (PPP-BOT)** | Optimization of crowd flow warning lights, obtaining real-time telecommunications signaling data. |

# Competitive Advantage (vs. Government Crowd Alert System)

| Item | Crowd Magnifier | Government Warning Lights |
| :--- | :--- | :--- |
| **Crowd Flow Info** | Future 24-hour prediction | Real-time only |
| **Attraction Coverage** | Thousands of attractions (full API fetch) | Only dozens of famous attractions |
| **Decision Support** | Risk index + alternative attraction suggestions | Only red/yellow/green lights |
| **Usage Threshold** | One-click query via LINE | Requires opening a webpage |
| **Cultural Value** | Includes attraction stories | None |

Strategic Interaction Problem:
Government green light → crowds rush in → turns red

CrowdLens Solution:
Addresses this issue with “prediction + alternative recommendations”


# Future Plan
| Direction | Plan |
| :--- | :--- |
| 1. Extend Prediction | To 1 week ~ 1 month (requires more historical data) |
| 2. Real-time Prediction | Partner with telecom companies to obtain signaling data |
| 3. Traffic Integration | Roadblocks, traffic jams, MRT real-time information |
| 4. Nationwide Expansion | Break through Taipei-New Taipei limitation |
| 5. Multilingual Versions | English and Japanese |
| 6. Store Recommendation | Paid priority push via algorithm |
| 7. APP/Web | Develop standalone versions |

# Contribution
| Aspect | Contribution |
| :--- | :--- |
| **Epidemic Prevention** | Avoid crowds and reduce transmission risk |
| **Cultural Promotion** | Promote attraction stories to enhance cultural identity |
| **Tech for Public Convenience** | One-click LINE query with integrated multi-source information |
