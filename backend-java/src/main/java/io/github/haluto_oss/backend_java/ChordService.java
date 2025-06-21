package io.github.haluto_oss.backend_java;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestTemplate;

import java.util.Map;

@Service // このクラスがビジネスロジックを担うサービスクラスであることを示す
public class ChordService {

    // Springに管理されているRestTemplateを自動的に注入してもらう
    @Autowired
    private RestTemplate restTemplate;

    // PythonのAPIサーバーのベースURL
    private final String pythonApiBaseUrl = "http://localhost:8000";

    // コードを分析するメソッド
    public Map<String, Object> analyzeChord(String chordName) {
        // 呼び出すPython APIの完全なURLを組み立てる
        String url = pythonApiBaseUrl + "/ai/analyze/chord/" + chordName;

        // Python APIを呼び出し、結果をMapとして受け取る
        // 2番目の引数 `Map.class` は、JSON応答をJavaのMapに自動変換するための指定
        return restTemplate.getForObject(url, Map.class);
    }
}