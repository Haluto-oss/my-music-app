package io.github.haluto_oss.backend_java;

import java.util.List;

// レコード(record)は、データを保持する目的のシンプルなクラスを簡潔に書くための機能です
public record FamousProgression(
    String name,
    String description,
    String key,
    List<String> chords
) {}