import cv2
import numpy as np
import logging

log = logging.getLogger("moon.vision")


class VisionSystem:
    """
    Vision module for:
      - object detection (YOLOv3 placeholder)
      - face recognition (OpenCV/DeepFace placeholder)
      - color detection
    """

    def __init__(self):
        # YOLO model placeholders
        self.net = None
        self.layer_names = None
        self.classes = None
        self._load_yolo()

    def _load_yolo(self):
        """
        Load YOLOv3 model (requires weights + cfg + coco.names).
        Paths are placeholders until you download them.
        """
        try:
            weights = "models/yolov3.weights"  # TODO: put actual path
            config = "models/yolov3.cfg"       # TODO: put actual path
            names = "models/coco.names"        # TODO: put actual path

            # Load network
            self.net = cv2.dnn.readNet(weights, config)
            self.layer_names = self.net.getLayerNames()
            self.layer_names = [self.layer_names[i - 1] for i in self.net.getUnconnectedOutLayers()]
            with open(names, "r") as f:
                self.classes = [line.strip() for line in f.readlines()]

            log.info("YOLO model loaded with %d classes", len(self.classes))
        except Exception:
            log.warning("YOLO not loaded (placeholders in use).")

    def detect_objects(self, frame):
        """Run YOLO object detection on a single frame. Returns list of labels."""
        if self.net is None or self.classes is None:
            log.warning("YOLO not available. Returning placeholder result.")
            return ["object_placeholder"]

        try:
            blob = cv2.dnn.blobFromImage(frame, 1 / 255.0, (416, 416), swapRB=True, crop=False)
            self.net.setInput(blob)
            outputs = self.net.forward(self.layer_names)

            H, W = frame.shape[:2]
            boxes, confidences, class_ids = [], [], []
            for out in outputs:
                for detection in out:
                    scores = detection[5:]
                    class_id = int(np.argmax(scores))
                    confidence = scores[class_id]
                    if confidence > 0.5:
                        box = detection[0:4] * np.array([W, H, W, H])
                        (centerX, centerY, width, height) = box.astype("int")
                        x = int(centerX - (width / 2))
                        y = int(centerY - (height / 2))
                        boxes.append([x, y, int(width), int(height)])
                        confidences.append(float(confidence))
                        class_ids.append(class_id)

            indices = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)
            results = [self.classes[class_ids[i]] for i in indices.flatten()]
            log.info("Objects detected: %s", results)
            return results
        except Exception:
            log.exception("Object detection failed.")
            return []

    def recognize_faces(self, frame):
        """
        Face recognition placeholder.
        TODO: Integrate with DeepFace or face_recognition.
        """
        try:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
            faces = face_cascade.detectMultiScale(gray, 1.3, 5)
            log.info("Detected %d faces", len(faces))
            return [f"face_{i}" for i, _ in enumerate(faces)]
        except Exception:
            log.exception("Face recognition failed.")
            return []

    def detect_colors(self, frame, x: int, y: int) -> str:
        """Return the closest color name at pixel (x,y)."""
        try:
            b, g, r = frame[y, x]
            color = f"R{r} G{g} B{b}"
            log.info("Color at (%d,%d): %s", x, y, color)
            return color
        except Exception:
            log.exception("Color detection failed.")
            return "unknown"
