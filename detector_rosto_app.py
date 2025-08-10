import cv2
import os

# --- Main Application Logic ---
def main():
    """Main function to run the face detection application."""
    casc_path = os.path.join(cv2.data.haarcascades, "haarcascade_frontalface_default.xml")

    if not os.path.exists(casc_path):
        print(f"Error: Could not find Haar Cascade model at {casc_path}")
        return

    face_cascade = cv2.CascadeClassifier(casc_path)
    if face_cascade.empty():
        print("Error: Failed to load Haar Cascade classifier.")
        return

    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Could not open camera.")
        return

    print("\nStarting camera. Press 'q' to exit.")
    print("Look for two windows: one with color, one in grayscale.")

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # --- Use the most permissive detection settings ---
        faces = face_cascade.detectMultiScale(
            gray,
            scaleFactor=1.05, # Check more scales
            minNeighbors=1,   # Be very lenient
            minSize=(30, 30)
        )

        # --- Draw rectangles and print status ---
        if len(faces) > 0:
            print(f"SUCCESS! Found {len(faces)} face(s)!")
            for (x, y, w, h) in faces:
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 3) # Thicker rectangle
        else:
            print("Still looking for faces...")

        # --- Display both color and grayscale frames ---
        cv2.imshow('Color Feed - Face Detector', frame)
        cv2.imshow('Grayscale Feed (What the AI Sees)', gray)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    print("Application closed.")

if __name__ == "__main__":
    main()