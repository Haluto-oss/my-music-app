package io.github.haluto_oss.backend_java;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.boot.web.client.RestTemplateBuilder;
import org.springframework.context.annotation.Bean;
import org.springframework.http.converter.json.MappingJackson2HttpMessageConverter; // <--- このimport文が重要
import org.springframework.web.client.RestTemplate;

@SpringBootApplication
public class BackendJavaApplication {

    public static void main(String[] args) {
        SpringApplication.run(BackendJavaApplication.class, args);
    }

    // ↓↓↓↓↓↓ このメソッドを、JSON変換機を確実に組み込む形に修正します ↓↓↓↓↓↓
    @Bean
    public RestTemplate restTemplate(RestTemplateBuilder builder) {
        return builder
                // RestTemplateに、JSONメッセージコンバーターを追加して、
                // MapオブジェクトからJSON文字列への変換を確実に行うようにする
                .additionalMessageConverters(new MappingJackson2HttpMessageConverter())
                .errorHandler(new RestTemplateResponseErrorHandler())
                .build();
    }
}