#version 330

layout (location = 0) in vec3 position;
layout (location = 1) in vec3 color;
layout (location = 2) in vec3 normal;

out vec4 vColor;
out vec3 vNormal;


uniform vec4 lightPosition;
uniform vec3 viewerPosition;

// model-view-projection matrix

uniform mat4 p3d_ModelMatrix;
uniform mat4 p3d_ViewMatrix;
uniform mat4 p3d_ProjectionMatrix;


uniform vec4 lightColor;

// these are properties of the OBJECT
uniform struct {
  vec4 ambient;
  vec4 diffuse;
  vec4 emission;
  vec3 specular;
  float shininess;
} p3d_Material;

void main()
{
    gl_Position = p3d_ProjectionMatrix * p3d_ViewMatrix * p3d_ModelMatrix * vec4(position, 1.0);

    vec3 pos = vec3(p3d_ModelMatrix * vec4(position, 1.0));

    vNormal = normalize(mat3(transpose(inverse(p3d_ModelMatrix))) * normal);  // need to check: its normal matrix...


    // ambient component
    float ambientStrength = 0.2;
    vec4 ambient = ambientStrength * p3d_Material.ambient * lightColor;



    vec3 lightDir;

    if (lightPosition[3] == 0.0)    // directional light
        lightDir = normalize(lightPosition.xyz);
    else
        lightDir = normalize(lightPosition.xyz - pos);

    // diffuse component

    float diff = max(dot(vNormal, lightDir), 0.0);

    vec4 diffuse = diff * p3d_Material.diffuse * lightColor;

    // specular
    float specularStrength = 0.5;
    vec3 viewDir = normalize(viewerPosition - pos);
    vec3 reflectDir = reflect(lightDir, vNormal);
    float spec = pow(max(dot(viewDir, reflectDir), 0.0), p3d_Material.shininess);

    vec3 lightColorV3 = lightColor.xyz;
    vec3 specularV3 = specularStrength * spec * p3d_Material.specular * lightColorV3;
    vec4 specular = vec4(specularV3, 0);

    // something needs to be done, here
    vColor = ambient + diffuse + specular;
}