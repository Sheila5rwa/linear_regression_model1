import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';

void main() {
  runApp(const AgriSmartApp());
}

class AgriSmartApp extends StatelessWidget {
  const AgriSmartApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'AgriSmart Africa',
      theme: ThemeData(
        colorScheme: ColorScheme.fromSeed(seedColor: Colors.green),
        useMaterial3: true,
      ),
      home: const PredictionScreen(),
      debugShowCheckedModeBanner: false,
    );
  }
}

class PredictionScreen extends StatefulWidget {
  const PredictionScreen({super.key});

  @override
  State<PredictionScreen> createState() => _PredictionScreenState();
}

class _PredictionScreenState extends State<PredictionScreen> {
  // Controllers for the input fields
  final TextEditingController _rainController = TextEditingController();
  final TextEditingController _tempController = TextEditingController();
  final TextEditingController _pesticideController = TextEditingController();

  bool _isLoading = false;
  String _resultText = '';

  // Your Render API URL
  final String apiUrl = 'https://linear-regression-model1.onrender.com/predict';

  Future<void> _predictYield() async {
    // Validate inputs
    if (_rainController.text.isEmpty ||
        _tempController.text.isEmpty ||
        _pesticideController.text.isEmpty) {
      setState(() {
        _resultText = 'Please fill in all fields.';
      });
      return;
    }

    setState(() {
      _isLoading = true;
      _resultText = '';
    });

    try {
      // Construct the exact JSON payload expected by FastAPI
      final Map<String, dynamic> requestData = {
        "average_rain_fall_mm_per_year": double.parse(_rainController.text),
        "avg_temp": double.parse(_tempController.text),
        "pesticides_tonnes": double.parse(_pesticideController.text)
      };

      // Make the POST request
      final response = await http.post(
        Uri.parse(apiUrl),
        headers: {"Content-Type": "application/json"},
        body: jsonEncode(requestData),
      );

      if (response.statusCode == 200) {
        final Map<String, dynamic> responseData = jsonDecode(response.body);
        final yieldResult = responseData['predicted_yield_hg_ha'];
        setState(() {
          _resultText = 'Predicted Yield:\n$yieldResult hg/ha';
        });
      } else {
        // Handle validation errors or server errors
        final errorData = jsonDecode(response.body);
        setState(() {
          _resultText = 'Error: ${errorData['detail']}';
        });
      }
    } catch (e) {
      setState(() {
        _resultText = 'Failed to connect to the server.\nCheck your internet or API URL.';
      });
    } finally {
      setState(() {
        _isLoading = false;
      });
    }
  }

  @override
  void dispose() {
    _rainController.dispose();
    _tempController.dispose();
    _pesticideController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text(
          'AgriSmart Yield Predictor',
          style: TextStyle(fontWeight: FontWeight.bold, color: Colors.white),
        ),
        backgroundColor: Colors.green[700],
        elevation: 0,
      ),
      body: SafeArea(
        child: SingleChildScrollView(
          padding: const EdgeInsets.all(24.0),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.stretch,
            children: [
              const Icon(Icons.eco, size: 80, color: Colors.green),
              const SizedBox(height: 16),
              const Text(
                'Enter farm metrics below to forecast the upcoming crop yield.',
                textAlign: TextAlign.center,
                style: TextStyle(fontSize: 16, color: Colors.black87),
              ),
              const SizedBox(height: 32),
              
              // Rainfall Input
              TextField(
                controller: _rainController,
                keyboardType: const TextInputType.numberWithOptions(decimal: true),
                decoration: InputDecoration(
                  labelText: 'Annual Rainfall (mm)',
                  hintText: 'e.g. 1200',
                  prefixIcon: const Icon(Icons.water_drop),
                  border: OutlineInputBorder(borderRadius: BorderRadius.circular(12)),
                ),
              ),
              const SizedBox(height: 16),

              // Temperature Input
              TextField(
                controller: _tempController,
                keyboardType: const TextInputType.numberWithOptions(decimal: true),
                decoration: InputDecoration(
                  labelText: 'Average Temperature (°C)',
                  hintText: 'e.g. 24.5',
                  prefixIcon: const Icon(Icons.thermostat),
                  border: OutlineInputBorder(borderRadius: BorderRadius.circular(12)),
                ),
              ),
              const SizedBox(height: 16),

              // Pesticides Input
              TextField(
                controller: _pesticideController,
                keyboardType: const TextInputType.numberWithOptions(decimal: true),
                decoration: InputDecoration(
                  labelText: 'Pesticides Used (tonnes)',
                  hintText: 'e.g. 150',
                  prefixIcon: const Icon(Icons.science),
                  border: OutlineInputBorder(borderRadius: BorderRadius.circular(12)),
                ),
              ),
              const SizedBox(height: 32),

              // Predict Button
              SizedBox(
                height: 56,
                child: ElevatedButton(
                  onPressed: _isLoading ? null : _predictYield,
                  style: ElevatedButton.styleFrom(
                    backgroundColor: Colors.green[700],
                    shape: RoundedRectangleBorder(
                      borderRadius: BorderRadius.circular(12),
                    ),
                  ),
                  child: _isLoading
                      ? const CircularProgressIndicator(color: Colors.white)
                      : const Text(
                          'Predict Yield',
                          style: TextStyle(fontSize: 18, color: Colors.white, fontWeight: FontWeight.bold),
                        ),
                ),
              ),
              const SizedBox(height: 32),

              // Result Display
              if (_resultText.isNotEmpty)
                Container(
                  padding: const EdgeInsets.all(20),
                  decoration: BoxDecoration(
                    color: Colors.green[50],
                    borderRadius: BorderRadius.circular(12),
                    border: Border.all(color: Colors.green.shade200),
                  ),
                  child: Text(
                    _resultText,
                    textAlign: TextAlign.center,
                    style: TextStyle(
                      fontSize: 20,
                      fontWeight: FontWeight.bold,
                      color: Colors.green[900],
                    ),
                  ),
                ),
            ],
          ),
        ),
      ),
    );
  }
}