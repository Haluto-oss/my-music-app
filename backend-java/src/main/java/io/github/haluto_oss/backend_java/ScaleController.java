// package io.github.haluto_oss.backend_java;

// import org.springframework.beans.factory.annotation.Autowired;
// import org.springframework.http.HttpHeaders;
// import org.springframework.http.ResponseEntity;
// import org.springframework.web.bind.annotation.*;
// import org.springframework.web.client.HttpClientErrorException;

// import java.util.Map;

// @RestController
// @RequestMapping("/api/scales") // このコントローラーは /api/scales で始まるURLを処理する
// public class ScaleController {

//     @Autowired
//     private ScaleService scaleService;

//     @CrossOrigin(origins = "http://localhost:5173")
//     @GetMapping // /api/scales?name=... というURLでこれが呼ばれる
//     public ResponseEntity<?> getScaleAnalysis(@RequestParam String name) {
//         System.out.println("★ Java ScaleController received with query: " + name);
//         try {
//             // ScaleServiceに実際の処理を依頼する
//             Map<String, Object> result = scaleService.analyzeScale(name);

//             // 成功した場合、キャッシュ無効化ヘッダーを付けて結果を返す
//             return ResponseEntity.ok()
//                     .header(HttpHeaders.CACHE_CONTROL, "no-cache, no-store, must-revalidate")
//                     .header(HttpHeaders.PRAGMA, "no-cache")
//                     .header(HttpHeaders.EXPIRES, "0")
//                     .body(result);

//         } catch (HttpClientErrorException e) {
//             // Pythonサーバーからエラーが返ってきた場合、そのエラーをそのままフロントエンドに返す
//             return ResponseEntity.status(e.getStatusCode()).body(e.getResponseBodyAsString());
//         }
//     }
// }

package io.github.haluto_oss.backend_java;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api/scales")
public class ScaleController {

    @Autowired
    private ScaleService scaleService;

    @CrossOrigin(origins = "http://localhost:5173")
    @GetMapping
    public String getScaleAnalysis(@RequestParam String name) {
        System.out.println("★ Java ScaleController received with query: " + name);
        // Serviceから受け取った文字列を、何もせずにそのままフロントエンドに返す
        return scaleService.analyzeScale(name);
    }
}