{{/*
Helper template for chart names
*/}}

{{- define "edc.name" -}}
{{- default .Chart.Name .Values.nameOverride | trunc 63 | trimSuffix "-" -}}
{{- end -}}

{{- define "edc.fullname" -}}
{{- printf "%s-%s" (include "edc.name" .) .Values.role | trunc 63 | trimSuffix "-" -}}
{{- end -}}