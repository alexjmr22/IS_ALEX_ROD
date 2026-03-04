package pt.uc.eai.model;
import java.util.List;

public class Payload {
    private String stream_id;
    private long timestamp;
    private List<Chunk> chunks;

    public Payload(){}
    
    public Payload(String stream_id, long timestamp, List<Chunk> chunks){
        this.stream_id = stream_id;
        this.timestamp = timestamp;
        this.chunks = chunks;
    }


    public String getStreamId() {
        return stream_id;
    }

    public void setStreamId(String stream_id) {
        this.stream_id = stream_id;
    }

    public long getTimestamp() {
        return timestamp;
    }

    public void setTimestamp(long timestamp) {
        this.timestamp = timestamp;
    }

    public List<Chunk> getChunks() {
        return chunks;
    }

    public void setChunks(List<Chunk> chunks) {
        this.chunks = chunks;
    }
}
