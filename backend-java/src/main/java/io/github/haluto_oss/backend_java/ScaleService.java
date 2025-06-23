// package io.github.haluto_oss.backend_java;

// import org.springframework.beans.factory.annotation.Autowired;
// import org.springframework.core.ParameterizedTypeReference;
// import org.springframework.http.HttpMethod;
// import org.springframework.http.ResponseEntity;
// import org.springframework.stereotype.Service;
// import org.springframework.web.client.RestTemplate;
// import org.springframework.web.util.UriComponentsBuilder;

// import java.util.Map;

// @Service
// public class ScaleService {

//     @Autowired
//     private RestTemplate restTemplate;

//     private final String pythonApiBaseUrl = "http://localhost:8000";

//     public Map<String, Object> analyzeScale(String scaleName) {
//         // PythonのAPIを呼び出すためのURLを、クエリパラメータ形式で安全に組み立てる
//         String url = UriComponentsBuilder.fromHttpUrl(pythonApiBaseUrl)
//                 .path("/ai/analyze/scale")
//                 .queryParam("name", scaleName)
//                 .toUriString();

//         // Python APIを呼び出し、結果をMapとして受け取る
//         ResponseEntity<Map<String, Object>> response = restTemplate.exchange(
//                 url,
//                 HttpMethod.GET,
//                 null,
//                 new ParameterizedTypeReference<Map<String, Object>>() {}
//         );

//         return response.getBody();
//     }
// }

package io.github.haluto_oss.backend_java;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestTemplate;
import org.springframework.web.util.UriComponentsBuilder;

@Service
public class ScaleService {

    @Autowired
    private RestTemplate restTemplate;

    private final String pythonApiBaseUrl = "http://localhost:8000";

    /**
     * デバッグのため、戻り値の型をMapからStringに変更します。
     * Pythonからの応答をそのまま文字列として返します。
     */
    public String analyzeScale(String scaleName) {
        // PythonのAPIを呼び出すためのURLを、クエリパラメータ形式で安全に組み立てる
        String url = UriComponentsBuilder.fromHttpUrl(pythonApiBaseUrl)
                .path("/ai/analyze/scale")
                .queryParam("name", scaleName)
                .toUriString();

        // 結果を加工せず、生のJSON文字列として受け取る
        return restTemplate.getForObject(url, String.class);
    }
}