package io.github.haluto_oss.backend_java;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestTemplate;
import java.util.List;
import java.util.Map;

@Service
public class TranspositionService {

    @Autowired
    private RestTemplate restTemplate;

    @Value("${python.api.base.url:http://localhost:8000}")
    private String pythonApiBaseUrl;

    /**
     * Pythonの移調APIを呼び出す
     * @param keyName 移調先のキー (例: "D")
     * @param degrees ディグリーネームのリスト (例: ["I", "V", "vi"])
     * @return 移調されたコードネームのリスト (例: ["D", "A", "Bm"])
     */
    @SuppressWarnings("unchecked")
    public List<String> transpose(String keyName, List<String> degrees) {
        String url = pythonApiBaseUrl + "/ai/transpose";

        // Pythonに送るリクエストのデータを作成
        Map<String, Object> requestBody = Map.of(
            "key_name", keyName,
            "degrees", degrees
        );

        // Python APIにPOSTリクエストを送信し、結果を受け取る
        Map<String, Object> response = restTemplate.postForObject(url, requestBody, Map.class);
        
        // 結果のMapから、"transposed_chords"というキーでリストを取り出して返す
        return (List<String>) response.get("transposed_chords");
    }
}