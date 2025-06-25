package io.github.haluto_oss.backend_java;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.core.ParameterizedTypeReference;
import org.springframework.http.HttpMethod;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestTemplate;
import org.springframework.web.util.UriComponentsBuilder;
import org.springframework.beans.factory.annotation.Value;

import java.util.Map;

@Service
public class ChordService {

    @Autowired
    private RestTemplate restTemplate;

    // ↓↓↓↓↓↓ この行を、@Valueを使うように変更します ↓↓↓↓↓↓
    @Value("${python.api.base.url:http://localhost:8000}")
    private String pythonApiBaseUrl;

    public Map<String, Object> analyzeChord(String chordName) {
        // UriComponentsBuilderを使って、URLエンコーディングの問題を安全に解決する
        String url = UriComponentsBuilder.fromHttpUrl(pythonApiBaseUrl)
                .path("/ai/analyze/chord")
                .queryParam("name", chordName) // <-- pathの代わりにqueryParamを使う
                .toUriString(); // <-- 文字列に戻してもクエリパラメータなら安全

        // getForObjectの代わりにexchangeメソッドを使い、期待する型を正確に伝える
        ResponseEntity<Map<String, Object>> response = restTemplate.exchange(
                url,
                HttpMethod.GET,
                null,
                new ParameterizedTypeReference<Map<String, Object>>() {}
        );

        return response.getBody();
    }
}