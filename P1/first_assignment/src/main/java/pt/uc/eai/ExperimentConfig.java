package pt.uc.eai;

import pt.uc.eai.Forma.SerializationFormat;

public class ExperimentConfig {

    private final SerializationFormat format;
    private final int numChunks;
    private final int framesPerChunk;

    public ExperimentConfig(SerializationFormat format, int numChunks, int framesPerChunk) {
        this.format = format;
        this.numChunks = numChunks;
        this.framesPerChunk = framesPerChunk;
    }

    public SerializationFormat getFormat() { return format; }
    public int getNumChunks() { return numChunks; }
    public int getFramesPerChunk() { return framesPerChunk; }

    @Override
    public String toString() {
        return String.format("ExperimentConfig{format=%s, numChunks=%d, framesPerChunk=%d}",
                format, numChunks, framesPerChunk);
    }
}
