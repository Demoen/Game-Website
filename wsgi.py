from game import app

if __name__ == "__main__":
    # This block is executed when the script is run directly, not when imported as a module.
    app.run(debug=True)  # You can specify host and port here, e.g., app.run(host='0.0.0.0', port=5000)