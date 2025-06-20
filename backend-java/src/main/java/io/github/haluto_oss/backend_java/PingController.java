package io.github.haluto_oss.backend_java;

import org.springframework.web.bind.annotation.CrossOrigin;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class PingController {

    // フロントエンド(http://localhost:3000)からのアクセスを許可する設定
    @CrossOrigin(origins = "http://localhost:3000")
    @GetMapping("/api/ping")
    public String ping() {
        return "Pong from Java! (Javaからの返事です)";
    }
}