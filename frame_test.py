def create_frames(no_frames, pixels_per_frame):
  frames = {}
  for x in range(no_frames):
    for y in range(pixels_per_frame):
      frame = []
      first_pixel = x * pixels_per_frame
      last_pixel = first_pixel + 29
      for pixel in range(first_pixel, last_pixel + 1):
        frame.append(pixel)
    frames[x] = frame
  return frames

frames = create_frames(4, 30)

print(frames)