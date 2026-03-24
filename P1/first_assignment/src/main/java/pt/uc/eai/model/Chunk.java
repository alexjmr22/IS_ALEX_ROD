package pt.uc.eai.model;
import java.util.List;

public class Chunk {
    private String chunk_id;
    private List<Frame> frames;

    public Chunk() {}

    public Chunk(String chunk_id, List<Frame> frames) {
        this.chunk_id = chunk_id;
        this.frames = frames;
    }

    public String getChunkId() {
        return chunk_id;
    }

    public void setChunkId(String chunk_id) {
        this.chunk_id = chunk_id;
    }

    public List<Frame> getFrames() {
        return frames;
    }

    public void setFrames(List<Frame> frames) {
        this.frames = frames;
    }
}
