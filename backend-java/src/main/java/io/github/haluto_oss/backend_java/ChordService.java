package io.github.haluto_oss.backend_java;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestTemplate;
import org.springframework.core.ParameterizedTypeReference; // <--- 追加
import org.springframework.http.HttpMethod; // <--- 追加
import org.springframework.http.ResponseEntity; // <--- 追加

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
        String url = pythonApiBaseUrl + "/ai/analyze/chord/" + chordName;
        // getForObjectの代わりにexchangeメソッドを使い、期待する型を正確に伝える
        ResponseEntity<Map<String, Object>> response = restTemplate.exchange(
                url,
                HttpMethod.GET,
                null, // GETリクエストなのでリクエストボディは無し
                new ParameterizedTypeReference<Map<String, Object>>() {}
        );
        
        return response.getBody();
    }
}