#include <Adafruit_MLX90614.h>

Adafruit_MLX90614 mlx = Adafruit_MLX90614();

void setup() {
  Serial.begin(9600);
	while (!Serial);

	if (!mlx.begin()) {
		Serial.println("Error connecting to MLX sensor.");
		while (1);
	};
}

void loop() {
	Serial.print("Ambient = "); Serial.print(mlx.readAmbientTempC());
	Serial.print("*C\tObject = "); Serial.print(mlx.readObjectTempC()); Serial.println("*C");

	Serial.println();
	delay(500);
}