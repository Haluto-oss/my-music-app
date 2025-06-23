package io.github.haluto_oss.backend_java;

import org.springframework.http.client.ClientHttpResponse;
import org.springframework.web.client.DefaultResponseErrorHandler;
import org.springframework.web.client.HttpClientErrorException;

import java.io.IOException;

public class RestTemplateResponseErrorHandler extends DefaultResponseErrorHandler {

    @Override
    public boolean hasError(ClientHttpResponse response) throws IOException {
        // デフォルトでは4xxと5xx系をエラーとして扱うが、ここでは4xx系のみを後続のhandleErrorで処理させたい
        // そのため、5xx系の場合はここでfalseを返し、デフォルトのエラー処理（例外をスロー）に任せる
        return response.getStatusCode().is5xxServerError();
    }

    @Override
    public void handleError(ClientHttpResponse response) throws IOException {
        // hasErrorがtrueを返した場合（5xxエラー）にここが呼ばれる
        // 4xxエラーはここで処理されず、呼び出し元（Controller）にHttpClientErrorExceptionとしてスローされる
        super.handleError(response);
    }
}