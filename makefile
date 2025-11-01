# Compiler
CXX = g++
# Linker flags
LDFLAGS = $(shell pkg-config --libs allegro-5 allegro_main-5 allegro_font-5 allegro_ttf-5 allegro_image-5 allegro_audio-5 allegro_primitives-5 allegro_acodec-5)

SRC = main.cpp
TARGET = vm.o

all: $(TARGET)

$(TARGET): $(SRC)
	$(CXX) ./$(SRC) -o $(TARGET) $(LDFLAGS)

clean:
	rm -f $(TARGET)

.PHONY: all clean