import cv2  # type: ignore
import numpy as np # type: ignore

class VideoCompressor:

    def compress_frame(self, frame, quality):
        """JPEG compression for a single frame"""
        encode_param = [cv2.IMWRITE_JPEG_QUALITY, quality]
        _, buffer = cv2.imencode('.jpg', frame, encode_param)
        compressed = cv2.imdecode(buffer, 1)
        ratio = frame.nbytes / len(buffer)
        return compressed, ratio

    def create_test_video(self):
        """Create a simple animated video"""
        frames = []
        for i in range(100):
            frame = np.zeros((360, 480, 3), np.uint8)

            # Moving circle
            cv2.circle(frame, (50 + i*4, 180), 40, (0, 255, 0), -1)

            # Text
            cv2.putText(frame, f'Frame {i}', (200, 50),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

            frames.append(frame)
        return frames

    def demo_compression(self):
        print("Creating test video...")
        original_frames = self.create_test_video()

        # 1. Original
        print("\n1. Showing original video (Press 'q' to skip)")
        for frame in original_frames:
            cv2.imshow('Original Video', frame)
            if cv2.waitKey(30) & 0xFF == ord('q'):
                break

        # 2. High quality 90
        print("\n2. High Quality Compression (90)")
        for frame in original_frames:
            compressed, ratio = self.compress_frame(frame, 90)
            cv2.imshow("High Quality (90)", compressed)
            if cv2.waitKey(30) & 0xFF == ord('q'):
                break

        #3.Medium quality 50
        print("\n3. Medium Quality compression(50)")
        for frame in original_frames:
            compressed, ratio = self.compress_frame(frame,20)
            cv2.imshow("Medium Quality (50)", compressed)
            if cv2.waitKey(30) & 0xFF == ord('q'):
                break

        # 4. Low quality 20
        print("\n4. Low Quality Compression (20)")
        for frame in original_frames:
            compressed, ratio = self.compress_frame(frame, 20)
            cv2.imshow("Low Quality (20)", compressed)
            if cv2.waitKey(30) & 0xFF == ord('q'):
                break

        # 5. Temporal compression (I and P frames)
        print("\n5. Temporal Compression (I/P Frames)")
        keyframe_interval = 10

        for i, frame in enumerate(original_frames):
            if i % keyframe_interval == 0:
                # I-frame (full frame)
                compressed, _ = self.compress_frame(frame, 80)
                cv2.putText(compressed, "I-FRAME", (10, 30),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
            else:
                # P-frame (difference from previous)
                diff = cv2.absdiff(frame, original_frames[i-1])
                compressed, _ = self.compress_frame(diff, 60)
                cv2.putText(compressed, "P-FRAME", (10, 30),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)

            cv2.imshow("Temporal Compression (I/P frames)", compressed)
            if cv2.waitKey(50) & 0xFF == ord('q'):
                break
        
        cv2.destroyAllWindows()
        #Compression Statistics
        print("\nCompression Ratios:")
        for q in [90, 50, 20]:
            _, ratio = self.compress_frame(original_frames[0], q)
            print(f" Quality {q}: {ratio:.2f}x compression")

#Run the demo
if __name__ == "__main__":
    compressor = VideoCompressor()
    compressor.demo_compression()



        

            