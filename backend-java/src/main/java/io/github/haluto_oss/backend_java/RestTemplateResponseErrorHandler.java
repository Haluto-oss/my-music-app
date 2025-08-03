// ファイル名: RestTemplateResponseErrorHandler.java

package io.github.haluto_oss.backend_java;

import org.springframework.http.client.ClientHttpResponse;
import org.springframework.web.client.DefaultResponseErrorHandler;
import java.io.IOException;

// このクラスの目的は、RestTemplateが4xxや5xxエラーを例外としてスローするようにすることです
public class RestTemplateResponseErrorHandler extends DefaultResponseErrorHandler {

    // このメソッドをオーバーライドして、エラーがあるかどうかを判断するロジックを修正します
    @Override
    public boolean hasError(ClientHttpResponse response) throws IOException {
        // isError()メソッドは、ステータスコードが4xxか5xxの場合にtrueを返します
        // これにより、Pythonからの422エラーも正しく「エラー」として扱われます
        return response.getStatusCode().isError();
    }

    // handleErrorメソッドは、hasErrorがtrueを返した場合に呼ばれます
    // デフォルトの動作（例外をスローする）のままで良いため、オーバーライドは不要です
}