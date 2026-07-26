# 🌾 AgriSmart Africa: Crop Yield Predictor

> **Empowering African farmers with AI-driven crop yield predictions for climate resilience and economic planning**

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Flutter](https://img.shields.io/badge/Flutter-v3.12+-blue.svg)](https://flutter.dev)
[![Python](https://img.shields.io/badge/Python-3.11%2B-green.svg)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-green.svg)](https://fastapi.tiangolo.com)



## 🎯 Overview

**AgriSmart Africa** is an end-to-end agricultural prediction platform that leverages machine learning to help small-scale farmers in Africa optimize their crop yields. The system combines a high-performance Python API with a mobile-first Flutter application, making predictive analytics accessible to farmers regardless of technical expertise.

### Mission
AgriSmart Africa empowers local farmers with predictive agricultural technology to secure food production against unpredictable climate changes, enabling data-driven decision-making and economic planning.

## 🚜 Problem Statement

African farmers face critical challenges:
- **Unpredictable Harvests**: Climate variability makes yield forecasting difficult
- **Economic Risk**: Unable to plan investments and resources accurately
- **Limited Data Access**: Lack of tools to leverage climate and farming data

**Solution**: AgriSmart Africa uses a trained linear regression model to predict exact crop yields based on:
- Annual rainfall (mm/year)
- Average temperature (°C)
- Farming inputs and practices

## ✨ Key Features

- 🤖 **ML-Powered Predictions**: Accurate crop yield forecasts using scikit-learn
- 📱 **Mobile-First Design**: Flutter app optimized for smartphone users in remote areas
- ⚡ **REST API**: Fast, scalable FastAPI backend with comprehensive documentation
- 🔒 **Input Validation**: Strict data constraints to ensure prediction accuracy
- 🌐 **CORS Support**: Seamless integration across web and mobile platforms
- 📊 **Swagger UI**: Interactive API documentation for developers
- 🔄 **Background Tasks**: Asynchronous processing capabilities

## 🛠️ Technology Stack

### Backend
| Technology | Version | Purpose |
|-----------|---------|---------|
| **FastAPI** | 0.115+ | Web framework for REST API |
| **Python** | 3.11+ | Core language |
| **scikit-learn** | 1.4+ | Machine learning library |
| **Pydantic** | 2.8+ | Data validation |
| **joblib** | 1.4+ | Model serialization |
| **Uvicorn** | 0.30+ | ASGI server |

### Frontend
| Technology | Version | Purpose |
|-----------|---------|---------|
| **Flutter** | 3.12+ | Cross-platform mobile development |
| **Dart** | 3.12+ | Flutter programming language |
| **HTTP** | Latest | API communication |

## 📁 Project Structure

```
linear_regression_model/
├── README.md                          # This file
├── pyproject.toml                     # Python project configuration
│
├── summative/
│   ├── API/                          # Backend API
│   │   ├── prediction.py             # FastAPI application
│   │   ├── requirements.txt          # Python dependencies
│   │   ├── best_model.pkl            # Trained ML model
│   │   └── scaler.pkl                # Data scaler
│   │
│   ├── FlutterApp/                   # Mobile Application
│   │   ├── pubspec.yaml              # Flutter dependencies
│   │   ├── lib/
│   │   │   └── main.dart             # Flutter entry point
│   │   ├── test/                     # Widget tests
│   │   ├── android/                  # Android configuration
│   │   ├── ios/                      # iOS configuration
│   │   ├── linux/                    # Linux configuration
│   │   ├── macos/                    # macOS configuration
│   │   ├── windows/                  # Windows configuration
│   │   └── web/                      # Web configuration
│   │
│   └── linear_regression/
│       └── multivariate.ipynb        # Model training notebook
```

## 🚀 Installation

### Prerequisites
- **Python** 3.11 or higher
- **Flutter** 3.12 or higher
- **Git**
- **pip** or **pip-tools**

### Backend Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/linear_regression_model.git
   cd linear_regression_model
   ```

2. **Install Python dependencies**
   ```bash
   cd summative/API
   pip install -r requirements.txt
   # OR using pyproject.toml
   pip install -e ../../
   ```

3. **Verify model files exist**
   ```bash
   ls -la | grep -E '(best_model.pkl|scaler.pkl)'
   ```
   
   If missing, train the model using the Jupyter notebook:
   ```bash
   jupyter notebook ../linear_regression/multivariate.ipynb
   ```

### Frontend Setup

1. **Install Flutter dependencies**
   ```bash
   cd summative/FlutterApp
   flutter pub get
   ```

2. **Verify Flutter installation**
   ```bash
   flutter doctor
   ```

## 📱 Usage

### Running the Backend API

```bash
cd summative/API
uvicorn prediction:app --host 0.0.0.0 --port 8000 --reload
```

**Access the API:**
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`
- API Root: `http://localhost:8000`

### Running the Mobile App

```bash
cd summative/FlutterApp
flutter run
```

**Supported platforms:**
- Android (native)
- iOS (native)
- Linux
- macOS
- Windows
- Web

**For specific platform:**
```bash
# Android
flutter run -d <device-id>

# iOS
flutter run -d <device-id>

# Web
flutter run -d chrome

# Desktop
flutter run -d linux
```

### Making Predictions

#### Via API (cURL)
```bash
curl -X POST "http://localhost:8000/predict" \
  -H "Content-Type: application/json" \
  -d '{
    "average_rain_fall_mm_per_year": 800,
    "avg_temp": 25.5,
    "fertilizer_kg_per_hectare": 120,
    "organic_matter": 5.2
  }'
```

#### Via Python
```python
import requests

data = {
    "average_rain_fall_mm_per_year": 800,
    "avg_temp": 25.5,
    "fertilizer_kg_per_hectare": 120,
    "organic_matter": 5.2
}

response = requests.post("http://localhost:8000/predict", json=data)
print(response.json())
```

#### Via Flutter App
1. Launch the app on your device/emulator
2. Enter the required parameters:
   - Annual Rainfall (mm)
   - Average Temperature (°C)
   - Fertilizer (kg/ha)
   - Organic Matter (%)
3. Tap "Predict" to get the yield forecast

## 📚 API Documentation

### Endpoint: `/predict`

**Method:** `POST`

**Description:** Predict crop yield based on environmental and farming factors

**Request Body:**
```json
{
  "average_rain_fall_mm_per_year": 800,
  "avg_temp": 25.5,
  "fertilizer_kg_per_hectare": 120,
  "organic_matter": 5.2
}
```

**Parameter Constraints:**
| Parameter | Min | Max | Unit |
|-----------|-----|-----|------|
| Rainfall | 50 | 3500 | mm/year |
| Temperature | 1 | 40 | °C |
| Fertilizer | 0 | 500 | kg/ha |
| Organic Matter | 0 | 20 | % |

**Response (Success):**
```json
{
  "predicted_yield": 3875.42,
  "unit": "kg/hectare",
  "confidence": "high"
}
```

**Response (Error):**
```json
{
  "detail": "Validation error details"
}
```

**Status Codes:**
- `200`: Successful prediction
- `422`: Validation error (parameter out of range)
- `500`: Server error

### Endpoint: `/health`

**Method:** `GET`

**Description:** Health check endpoint

**Response:**
```json
{
  "status": "healthy",
  "model_loaded": true
}
```

## 🐛 Troubleshooting

### Backend Issues

**Issue: Model file not found**
```
FileNotFoundError: best_model.pkl not found
```
**Solution:**
- Train the model using the Jupyter notebook in `summative/linear_regression/`
- Save pickled files as `best_model.pkl` and `scaler.pkl` in the API directory

**Issue: CORS errors in Flutter app**
```
Error: Cross-Origin Request Blocked
```
**Solution:**
- Ensure the API server includes your Flutter app's origin in `ALLOWED_ORIGINS`
- For local testing, add `http://localhost:8080` and `http://127.0.0.1:8080`

**Issue: Port already in use**
```
OSError: [Errno 98] Address already in use
```
**Solution:**
```bash
# Use a different port
uvicorn prediction:app --host 0.0.0.0 --port 8001
```

### Frontend Issues

**Issue: Flutter pub get fails**
```
Error: Pub get failed
```
**Solution:**
```bash
flutter clean
flutter pub get
```

**Issue: Android build fails**
```
Error: SDK location not found
```
**Solution:**
```bash
flutter config --android-sdk /path/to/android/sdk
```

**Issue: Connection refused (API not reachable)**
```
Error: Failed to connect to localhost:8000
```
**Solution:**
- Verify API is running: `http://localhost:8000/docs`
- Check firewall settings
- Use the correct IP address (not `localhost` if running on different machines)
- For emulator, use `10.0.2.2:8000` instead of `localhost:8000`

## 🤝 Contributing

Contributions are welcome! Here's how to get started:

1. Fork the repository
2. Create a feature branch
   ```bash
   git checkout -b feature/amazing-feature
   ```
3. Make your changes
4. Commit with clear messages
   ```bash
   git commit -m "Add amazing feature"
   ```
5. Push to your branch
   ```bash
   git push origin feature/amazing-feature
   ```
6. Open a Pull Request

### Code Standards
- Follow PEP 8 for Python code
- Use type hints in Python functions
- Follow Dart style guide for Flutter code
- Add tests for new features
- Update documentation

## 📝 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## 👥 Authors

- **Your Name** - *Initial work* - [GitHub Profile](https://github.com/yourusername)

## 🔗 Useful Links

- [FastAPI Documentation](https://fastapi.tiangolo.com)
- [Flutter Documentation](https://flutter.dev/docs)
- [scikit-learn Guide](https://scikit-learn.org/stable/)
- [Dart Language Tour](https://dart.dev/guides/language/language-tour)

## 📞 Support

For issues, questions, or suggestions:
- Open an [Issue](https://github.com/yourusername/linear_regression_model/issues)
- Start a [Discussion](https://github.com/yourusername/linear_regression_model/discussions)
- Contact: your.email@example.com

---

**Last Updated:** July 2024 | **Status:** Active Development ✅
